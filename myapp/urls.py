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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
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
    path('rooms/<int:room_id>/', views.roomattendance, name='roomattendance'),

    path('courses/', views.admincourses, name='admincourses'),
    path('addcourse/', views.addcourse, name='addcourse'),
    path('deletecourse/', views.deletecourse, name='deletecourse'),
    path('courses/<int:course_id>/', views.courseattendance, name='courseattendance'),

    path('addstudent/<int:course_id>/', views.addstudent, name='addstudent'),
    path('deletestudent/<int:course_id>/', views.deletestudent, name='deletestudent'),

    path('login/', views.loginPage, name = 'login'),
    path('logout/', views.logoutUser, name = 'logout'),
]

urlpatterns += staticfiles_urlpatterns()