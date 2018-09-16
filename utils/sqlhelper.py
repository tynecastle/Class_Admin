import pymysql

def get_list(sql, args):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='0102', db='andreadb', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql, args)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_one(sql, args):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='0102', db='andreadb', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql, args)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def modify(sql, args):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='0102', db='andreadb', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql, args)
    conn.commit()
    cursor.close()
    conn.close()

def create(sql, args):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='0102', db='andreadb', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql, args)
    conn.commit()
    last_row_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return last_row_id

class Sqlapi(object):
    def __init__(self):
        self.connect()

    def connect(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='0102', db='andreadb', charset='utf8')
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def get_list(self,sql,args):
        self.cursor.execute(sql,args)
        return self.cursor.fetchall()

    def get_one(self,sql,args):
        self.cursor.execute(sql,args)
        return self.cursor.fetchone()

    def create(self,sql,args):
        self.cursor.execute(sql,args)
        self.conn.commit()
        return self.cursor.lastrowid

    def modify(self,sql,args):
        self.cursor.execute(sql,args)
        self.conn.commit()

    def multi_modify(self,sql,args):
        self.cursor.executemany(sql,args)
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()