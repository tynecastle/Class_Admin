from django.http import HttpResponse, Http404
import datetime, pymysql, json
from django.shortcuts import render, redirect
from utils import sqlhelper

def siteroot(request):
    return HttpResponse("Welcome to Django !")

def showtime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s</body></html>" % now
    return HttpResponse(html)

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    assert False
    html = "<html><body>In %s hour(s), it will be %s</body></html>" % (offset, dt)
    return HttpResponse(html)

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        usr = request.POST.get('username')
        pwd = request.POST.get('password')
        if usr == 'andrea' and pwd == '987654321':
            return redirect('/now/')
        else:
            return render(request, 'login.html', {'msg': 'wrong username or password'})

def index(request):
    return render(
        request,
        'index.html',
        {
            'name': 'Andrea',
            'users': ['Fred', 'Vicki'],
            'user_dict': {'k1':'v1', 'k2':'v2'},
            'user_list_dict': [
                {'id':1, 'name':'Lucy', 'gender':'F'},
                {'id':2, 'name':'Mike', 'gender':'M'},
                {'id':3, 'name':'Belle', 'gender':'F'},
            ]
        }
    )

def classes(request):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='0102', db='andreadb', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select cid,cname from class")
    class_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request, 'classes.html', {'class_list': class_list})

def add_class(request):
    if request.method == "GET":
        return render(request, 'add_class.html')
    else:
        class_name = request.POST.get('title')
        if len(class_name) > 0:
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='0102', db='andreadb', charset='utf8')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            cursor.execute("insert into class(cname) values(%s)", [class_name,])
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/classes/')
        else:
            return render(request, 'add_class.html', {'msg': '  invalid class name'})

def del_class(request):
    nid = request.GET.get('nid')
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='0102', db='andreadb', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("delete from class where cid=%s", [nid,])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/classes/')

def edit_class(request):
    if request.method == "GET":
        nid = request.GET.get('nid')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='0102', db='andreadb', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select cid,cname from class where cid=%s", [nid,])
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return render(request, 'edit_class.html', {'result': result})
    else:
        nid = request.GET.get('nid')
        title = request.POST.get('cname')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='0102', db='andreadb', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("update class set cname=%s where cid=%s", [title,nid,])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/classes/')

def students(request):
    student_list = sqlhelper.get_list('select sid,sname,classid,cname from student left join class on student.classid=class.cid', [])
    class_list = sqlhelper.get_list('select cid,cname from class', [])
    return render(request, 'students.html', {'student_list': student_list, 'class_list': class_list})

def add_student(request):
    if request.method == "GET":
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='0102', db='andreadb', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select cid,cname from class")
        class_list = cursor.fetchall()
        cursor.close()
        conn.close()
        return render(request, 'add_student.html', {'class_list': class_list})
    else:
        stuname = request.POST.get('stu_name')
        classid = request.POST.get('class_id')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='0102', db='andreadb', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("insert into student(sname,classid) values(%s,%s)", [stuname,classid,])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/students/')

def edit_student(request):
    if request.method == "GET":
        nid = request.GET.get('nid')
        class_list = sqlhelper.get_list('select cid,cname from class', [])
        curr_stu = sqlhelper.get_one('select sid,sname,classid from student where sid=%s', [nid,])
        return render(request, 'edit_student.html', {'class_list': class_list, 'curr_stu': curr_stu})
    else:
        nid = request.GET.get('nid')
        stuname = request.POST.get('sname')
        class_id = request.POST.get('class_id')
        sqlhelper.modify("update student set sname=%s,classid=%s where sid=%s", [stuname,class_id,nid])
        return redirect('/students/')

def modal_add_class(request):
    title = request.POST.get('title')
    if len(title) > 0:
        sqlhelper.modify('insert into class(cname) values(%s)', [title,])
        return HttpResponse('ok')
    else:
        return HttpResponse('empty class name is unaccepted')

def modal_edit_class(request):
    ret = {'status': True, 'message': None}
    try:
        nid = request.POST.get('nid')
        content = request.POST.get('content')
        sqlhelper.modify('update class set cname=%s where cid=%s', [content,nid,])
    except Exception as e:
        ret['status'] = False
        ret['message'] = 'Exception raised'
    return HttpResponse(json.dumps(ret))

def modal_add_student(request):
    ret = {'status': True, 'message': None}
    try:
        stuname = request.POST.get('stu_name')
        gender = request.POST.get('gender')
        classid = request.POST.get('class_id')
        sqlhelper.modify('insert into student(sname,gender,classid) values(%s,%s,%s)', [stuname,gender,classid,])
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
    return HttpResponse(json.dumps(ret))

def modal_edit_student(request):
    ret = {'status': True, 'message': None}
    try:
        nid = request.POST.get('nid')
        stuname = request.POST.get('stu_name')
        classid = request.POST.get('class_id')
        sqlhelper.modify('update student set sname=%s,classid=%s where sid=%s', [stuname,classid,nid,])
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
    return HttpResponse(json.dumps(ret))

def teachers(request):
    teacher_list = sqlhelper.get_list("""
        SELECT tid,tname,cname FROM teacher
        LEFT JOIN teacher2class ON teacher.tid = teacher2class.teacherid
        LEFT JOIN class ON teacher2class.classid = class.cid
    """, [])
    teacher_dict = {}
    for row in teacher_list:
        tid = row['tid']
        if tid in teacher_dict:
            teacher_dict[tid]['classes'].append(row['cname'])
        else:
            teacher_dict[tid] = {'tid': row['tid'], 'tname': row['tname'], 'classes': [row['cname'],]}
    return render(request, 'teachers.html', {'teacher_dict': teacher_dict.values()})

def add_teacher(request):
    if request.method == "GET":
        class_list = sqlhelper.get_list('select cid,cname from class', [])
        return render(request, 'add_teacher.html', {'class_list': class_list})
    else:
        tchrname = request.POST.get('tchr_name')
        tchrid = sqlhelper.create('insert into teacher(tname) values(%s)', [tchrname,])
        classids = request.POST.getlist('class_ids')

        ## multi-connects, multi-submits
        #for clsid in classids:
        #    sqlhelper.modify('insert into teacher2class(teacherid,classid) values(%s,%s)', [tchrid,clsid,])

        ## one-connect, multi-submits
        #sqlobj = sqlhelper.Sqlapi()
        #for clsid in classids:
        #    sqlobj.modify('insert into teacher2class(teacherid,classid) values(%s,%s)', [tchrid,clsid,])
        #sqlobj.close()

        ## one-connect, one-submit
        data_list = []
        for clsid in classids:
            data_list.append((tchrid,clsid,))
        sqlobj = sqlhelper.Sqlapi()
        sqlobj.multi_modify('insert into teacher2class(teacherid,classid) values(%s,%s)', data_list)
        sqlobj.close()
        return redirect('/teachers/')

def edit_teacher(request):
    if request.method == "GET":
        nid = request.GET.get('nid')
        sqlobj = sqlhelper.Sqlapi()
        tchrinfo = sqlobj.get_one('select tid,tname from teacher where tid=%s', [nid,])
        classlist = sqlobj.get_list('select cid,cname from class', [])
        classids_dicts = sqlobj.get_list('select classid from teacher2class where teacherid=%s', [nid,])
        classids = []
        for d in classids_dicts:
            classids.append(d['classid'])
        sqlobj.close()
        return render(request, 'edit_teacher.html', {
            'tchr_info': tchrinfo,
            'class_ids': classids,
            'class_list': classlist,
        })
    else:
        nid = request.GET.get('nid')
        tchrname = request.POST.get('tchr_name')
        classids = request.POST.getlist('class_ids')
        sqlobj = sqlhelper.Sqlapi()
        sqlobj.modify('update teacher set tname=%s where tid=%s', [tchrname,nid])
        sqlobj.modify('delete from teacher2class where teacherid=%s', [nid,])
        data_list = []
        for clsid in classids:
            data_list.append((nid,clsid,))
        sqlobj.multi_modify('insert into teacher2class(teacherid,classid) values(%s,%s)', data_list)
        sqlobj.close()
        return redirect('/teachers/')

def get_all_classes(request):
    import time
    time.sleep(2)
    sqlobj = sqlhelper.Sqlapi()
    classlist = sqlobj.get_list('select cid,cname from class', [])
    sqlobj.close()
    return HttpResponse(json.dumps(classlist))

def modal_add_teacher(request):
    ret = {'status': True, 'message': None}
    try:
        tchrname = request.POST.get('tchr_name')
        classids = request.POST.getlist('class_ids')
        sqlobj = sqlhelper.Sqlapi()
        tchrid = sqlobj.create('insert into teacher(tname) values(%s)', [tchrname,])
        data_list = []
        for clsid in classids:
            data_list.append((tchrid,clsid,))
        sqlobj.multi_modify('insert into teacher2class(teacherid,classid) values(%s,%s)', data_list)
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
    return HttpResponse(json.dumps(ret))

def test(request):
    return render(request, 'test.html')

def layout(request):
    return render(request, 'layout.html')
