"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from mysite import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.siteroot),
    url(r'^now/$', views.showtime),
    url(r'^time/plus/(\d{1,2})/$', views.hours_ahead),
    url(r'^login/', views.login),
    url(r'^index/', views.index),

    url(r'^classes/', views.classes),
    url(r'^add-class/', views.add_class),
    url(r'^del-class/', views.del_class),
    url(r'^edit-class/', views.edit_class),

    url(r'^students/', views.students),
    url(r'^add-student/', views.add_student),
    url(r'^edit-student/', views.edit_student),

    url(r'^modal-add-class/', views.modal_add_class),
    url(r'^modal-edit-class/', views.modal_edit_class),

    url(r'^modal-add-student/', views.modal_add_student),
    url(r'^modal-edit-student/', views.modal_edit_student),

    url(r'^teachers/', views.teachers),
    url(r'^add-teacher/', views.add_teacher),
    url(r'^edit-teacher/', views.edit_teacher),
    url(r'^get-all-classes/', views.get_all_classes),
    url(r'^modal-add-teacher/', views.modal_add_teacher),

    url(r'^test/', views.test),
    url(r'^layout/', views.layout),
]
