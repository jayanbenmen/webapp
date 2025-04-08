"""
URL configuration for mydjangosite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from .views import PasswordsChangeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.loginPage, name = 'login'),
    path('initial/', views.initial, name = 'initial'),
    path('registered/', views.registered, name = 'registered'),
    path('instudent/', views.instudent, name = 'instudent'),
    path('inteacher/', views.inteacher, name = 'inteacher'),
    path('inadmin/', views.inadmin, name='inadmin'),
    path('redirect/', views.role_redirect, name = 'role_redirect'),
    path('studenthome/', views.studenthome, name='studenthome'),
    path('teacherhome/', views.teacherhome, name='teacherhome'),
    path('adminhome/', views.adminhome, name='adminhome'),

    path('rooms/', views.adminrooms, name='adminrooms'),
    path('addroom/', views.addroom, name='addroom'),
    path('deleteroom/', views.deleteroom, name='deleteroom'),
    path('deleteroombutton/<int:room_id>/', views.deleteroombutton, name='deleteroombutton'),
    path('rooms/<int:room_id>/', views.roomattendance, name='roomattendance'),

    path('courses/', views.admincourses, name='admincourses'),
    path('addcourse/', views.addcourse, name='addcourse'),
    path('deletecourse/', views.deletecourse, name='deletecourse'),
    path('deletecoursebutton/<int:course_id>/', views.deletecoursebutton, name='deletecoursebutton'),
    path('courses/<int:course_id>/', views.courseattendance, name='courseattendance'),
    path('adminstudentlist/<int:course_id>/', views.adminstudentlist, name='adminstudentlist'),
    path('assign_teacher/<int:course_id>/', views.assign_teacher, name='assign_teacher'),

    path('addstudent/<int:course_id>/', views.addstudent, name='addstudent'),
    path('deletestudent/<int:course_id>/', views.deletestudent, name='deletestudent'),

    path('nfcuid/', views.nfcuid, name='nfcuid'),
    path('updteachernfc/<str:teacher_id>/', views.updteachernfc, name='updteachernfc'),
    path('updstudentnfc/<str:student_id>/', views.updstudentnfc, name='updstudentnfc'),

    # path('login/', views.loginPage, name = 'login'),
    path('logout/', views.logoutUser, name = 'logout'),

    path('password/', PasswordsChangeView.as_view(template_name = 'registration/change-password.html'), name = 'change-password'),
    path('password_success/', views.password_success, name = 'password_success'),
    path('goto_profile/', views.goto_profile, name = 'goto_profile'),

    path('teacher_profile/', views.teacher_profile, name = 'teacher_profile'),
    path('teacher_courses/', views.teacher_courses, name = 'teacher_courses'),
    path('studentattendance/<int:course_id>/', views.studentattendance, name = 'studentattendance'),
    path('teacherattendance/<int:course_id>/', views.teacherattendance, name = 'teacherattendance'),
    path('teacher_classlist/<int:course_id>/', views.teacher_classlist, name='teacher_classlist'),
    path('teacher_nfcupd/', views.teacher_nfcupd, name = 'teacher_nfcupd'),
    path('manual_attendance/<int:course_id>/', views.manual_attendance, name = 'manual_attendance'),

    path('student_profile/', views.student_profile, name = 'student_profile'),
    path('student_courses/', views.student_courses, name = 'student_courses'),
    path('attendance/<int:course_id>/', views.attendance, name = 'attendance'),
    path('student_nfcupd/', views.student_nfcupd, name = 'student_nfcupd'),

    # CSV
    path('students_monthly_attendance/<int:course_id>/', views.students_monthly_attendance, name = 'students_monthly_attendance'),
    path('monthly_room_logs/<int:room_id>/', views.monthly_room_logs, name = 'monthly_room_logs'),
]

urlpatterns += staticfiles_urlpatterns()