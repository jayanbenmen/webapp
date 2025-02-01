from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse

from .decorators import unauthenticated_user, allowed_users
from .models import Users
from .models import Students
from .models import Teachers
from .models import Admins
from .models import Rooms
from .models import Courses
from django.db import transaction
from django.contrib import messages
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from .forms import AdminCreationForm

# Create your views here.

def index(request):
    return render(request, "myapp/index.html", {})

def instudent(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST or None)

        outstudentid = form.data.get('username')
        outfirstname = form.data.get('first_name')
        outlastname = form.data.get('last_name')
        outemail = form.data.get('email')
        outpw1 = form.data.get('password1')
        outpw2 = form.data.get('password2')
        outnfcuid = request.POST['innfcuid']
        outusertype = "student"

        errors = []
        id_pattern = r'^CO20\d{7}$'

        if outstudentid == '' or outfirstname == '' or outlastname == '' or outemail == '' or outpw1 == '' or outpw2 == '':
            errors.append('Missing required fields')

        if not re.match(id_pattern,outstudentid):
            errors.append('Invalid Student ID e.g. (CO202100123)')

        if Students.objects.filter(student_id = outstudentid).exists():
            errors.append('Student ID already exists')

        if not is_valid_email(outemail):
            errors.append('Email format is invalid (@gbox.adnu.edu.ph)')

        if Users.objects.filter(email=outemail).exists():
            errors.append('Email already exists')

        if len(outpw1) < 8:
            errors.append('Password should atleast be 8 characters')

        if outpw1 != outpw2:
            errors.append('Passwords do not match')

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('instudent')


        messages.success(request, 'Account was created for  ' + outstudentid)
        au = User.objects.create_user(username=outstudentid,first_name = outfirstname, last_name = outlastname, email=outemail, password=outpw1)
        au.save()

        group = Group.objects.get(name='student')
        au.groups.add(group)

        us = Users(email = outemail, pw = outpw1, user_type = outusertype, au_user_id = au.id)
        us.save()
        outuserid = us.user_id
        st = Students(student_id=outstudentid, user_id=outuserid, first_name=outfirstname, last_name=outlastname, nfc_uid=outnfcuid)
        st.save()
        return redirect('login')
    return render(request, "registration/instudent.html", {"form": form})

def inteacher(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST or None)

        outteacherid = form.data.get('username')
        outfirstname = form.data.get('first_name')
        outlastname = form.data.get('last_name')
        outemail = form.data.get('email')
        outpw1 = form.data.get('password1')
        outpw2 = form.data.get('password2')
        outnfcuid = request.POST['innfcuid']
        outusertype = "teacher"

        errors = []
        id_pattern = r'^HR20\d{7}$'

        if outteacherid == '' or outfirstname == '' or outlastname == '' or outemail == '' or outpw1 == '' or outpw2 == '':
            errors.append('Missing required fields')

        if not re.match(id_pattern,outteacherid):
            errors.append('Invalid Teacher ID e.g. (HR202100123)')

        if Teachers.objects.filter(teacher_id = outteacherid).exists():
            errors.append('Teacher ID already exists')

        if not is_valid_email(outemail):
            errors.append('Email format is invalid (@gbox.adnu.edu.ph)')

        if Users.objects.filter(email=outemail).exists():
            errors.append('Email already exists')

        if len(outpw1) < 8:
            errors.append('Password should atleast be 8 characters')

        if outpw1 != outpw2:
            errors.append('Passwords do not match')

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('inteacher')

        messages.success(request, 'Account was created for  ' + outteacherid)
        au = User.objects.create_user(username=outteacherid,first_name = outfirstname, last_name = outlastname, email=outemail, password=outpw1)
        au.save()

        group = Group.objects.get(name='teacher')
        au.groups.add(group)

        us = Users(email=outemail, pw=outpw1, user_type=outusertype, au_user_id=au.id)
        us.save()
        outuserid = us.user_id
        te = Teachers(teacher_id=outteacherid, user_id=outuserid, first_name=outfirstname, last_name=outlastname, nfc_uid=outnfcuid)
        te.save()
        return redirect('login')
    return render(request, "registration/inteacher.html", {"form": form})

def inadmin(request):
    form = AdminCreationForm()
    if request.method == 'POST':
        form = AdminCreationForm(request.POST or None)

        outusername = form.data.get('username')
        outfirstname = form.data.get('first_name')
        outlastname = form.data.get('last_name')
        outemail = form.data.get('email')
        outpw1 = form.data.get('password1')
        outpw2 = form.data.get('password2')
        outusertype = "admin"

        errors = []

        if outusername == '' or outfirstname == '' or outlastname == '' or outemail == '' or outpw1 == '' or outpw2 == '':
            errors.append('Missing required fields')

        if Users.objects.filter(email=outemail).exists():
            errors.append('Email already exists')

        if len(outpw1) < 8:
            errors.append('Password should atleast be 8 characters')

        if outpw1 != outpw2:
            errors.append('Passwords do not match')

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('inadmin')

        messages.success(request, 'Account was created for  ' + outusername)
        su = User.objects.create_superuser(username = outusername, first_name = outfirstname, last_name = outlastname ,email = outemail, password = outpw1)
        su.save()

        group = Group.objects.get(name='admin')
        su.groups.add(group)

        us = Users(email=outemail, pw=outpw1, user_type=outusertype, au_user_id = su.id)
        us.save()
        outuserid = us.user_id
        ad = Admins(username=outusername, user_id=outuserid, first_name=outfirstname, last_name=outlastname)
        ad.save()
        return redirect('login')
    return render(request, "registration/inadmin.html", {"form": form})

def registered(request):
    return render(request, "registration/registered.html", {})

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
         username = request.POST.get('username')
         password = request.POST.get('password')

         user = authenticate(request, username = username, password = password)

         if user is not None:
             login(request, user)
             if user.groups.filter(name='student').exists():
                 return redirect('studenthome')
             elif user.groups.filter(name='teacher').exists():
                 return redirect('teacherhome')
             elif user.groups.filter(name='admin').exists():
                 return redirect('adminhome')

         else:
             messages.info(request, 'ID Number or Password is Incorrect')
             return render(request, "accounts/login.html", {})

    return render(request, "accounts/login.html", {})

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url = 'login')
def studenthome(request):
    student = None
    if hasattr(request.user, 'student'):
        student = request.user.student
    return render(request, "studentapp/studenthome.html",{'student': student})

@login_required(login_url = 'login')
def teacherhome(request):
    return render(request, "teacherapp/teacherhome.html",{})

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def adminhome(request):
    return render(request, "adminapp/adminhome.html",{})

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def adminrooms(request):
    rooms = Rooms.objects.all()
    return render(request, "adminapp/rooms.html",{'rooms': rooms})

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def roomattendance(request, room_id):
    room = get_object_or_404(Rooms, room_id = room_id)
    return render(request, "adminapp/roomattendance.html",{'room': room})

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def addroom(request):
    if request.method == "POST":
        outroomname = request.POST['inroomname']
        if not outroomname:
            return redirect('addroom')
        else:
            ro = Rooms(room_name = outroomname)
            ro.save()
            return redirect('adminrooms')
    return render(request, "adminapp/addroom.html",{})

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def deleteroom(request):
    if request.method == "POST":
        outroomname = request.POST['inroomname']
        errors = []


        if not outroomname:
            errors.append('Please input a room name')

        room = Rooms.objects.filter(room_name = outroomname).first()

        if room:
            if Courses.objects.filter(room_id = room.room_id):
                errors.append('Cannot delete, room is used in a Course')
        else:
            errors.append('Room does not exist')


        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('deleteroom')
        room.delete()
        return redirect('adminrooms')
    return render(request, "adminapp/deleteroom.html",{})

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def admincourses(request):
    courses = Courses.objects.all()
    return render(request, "adminapp/courses.html",{'courses': courses})

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def courseattendance(request, course_id):
    course = get_object_or_404(Courses, course_id = course_id)
    return render(request, "adminapp/courseattendance.html",{'course': course})

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def addcourse(request):
    if request.method == "POST":
            outcoursecode = request.POST['incoursecode']
            outcoursetitle = request.POST['incoursetitle']
            outsection = request.POST['insection']
            outstarttime = request.POST['instarttime']
            outendtime = request.POST['inendtime']
            outday = request.POST['inday']
            outroom =  request.POST['inroom']
            outteacherid = request.POST['inteacherid']

            errors = []

            room = Rooms.objects.filter(room_name=outroom).first()

            sched_conflict = Courses.objects.filter(
                room_id = room.room_id,
                schedule_day = outday
            ).filter(
                start_time__lt=outendtime,  # Existing course starts before new course ends
                end_time__gt=outstarttime  # Existing course ends after new course starts
            ).exists()

            subj_conflict = Courses.objects.filter(
                course_code = outcoursecode,
                section = outsection
            ).exists()

            teacher_exists = Teachers.objects.filter(teacher_id=outteacherid).exists()
            if not teacher_exists:
                errors.append('Teacher does not exist')

            if sched_conflict:
                errors.append('Conflict with existing courses in the same room')

            if subj_conflict:
                errors.append('Course and Section already exists')

            if errors:
                for error in errors:
                    messages.error(request, error)
                return redirect('addcourse')

            co = Courses(course_code=outcoursecode,
                         course_title=outcoursetitle,
                         section=outsection,
                         start_time=outstarttime,
                         end_time=outendtime,
                         schedule_day=outday,
                         room_id = room.room_id,
                         teacher_id = outteacherid,
                         )
            co.save()
            return redirect('admincourses')

    return render(request, "adminapp/addcourse.html",{})

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def deletecourse(request):
    if request.method == "POST":
        outcoursecode = request.POST['incoursecode']
        outsection = request.POST['insection']

        errors = []

        subj_exists = Courses.objects.filter(
            course_code=outcoursecode,
            section=outsection
        ).exists()

        if not outcoursecode or not outsection:
            errors.append('Missing required fields')

        if not subj_exists:
            errors.append('Course does not exist')

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('deleteroom')

        course = Courses.objects.filter(course_code = outcoursecode, section = outsection).first()
        course.delete()
        return redirect('admincourses')

    return render(request, "adminapp/deletecourse.html", {})

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def addstudent(request, course_id):
    course = get_object_or_404(Courses, course_id=course_id)

    if request.method == "POST":
        outstudentid = request.POST['instudentid']

        errors = []
        id_pattern = r'^CO20\d{7}$'

        student = Students.objects.filter(student_id = outstudentid).first()

        if not re.match(id_pattern,outstudentid):
            errors.append('Invalid Student ID e.g. (CO202100123)')

        if student:
            if course.students.filter(student_id = outstudentid).exists():
                errors.append('Student is already enrolled in this course')
            else:
                course.students.add(student)
                return redirect('courseattendance', course_id=course_id)
        else:
            errors.append('Student does not exist')

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('addstudent', course_id=course_id)

    return render(request, "adminapp/addstudent.html",{'course': course})

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def deletestudent(request, course_id):
    course = get_object_or_404(Courses, course_id=course_id)

    if request.method == "POST":
        outstudentid = request.POST['instudentid']

        errors = []
        id_pattern = r'^CO20\d{7}$'

        student = Students.objects.filter(student_id = outstudentid).first()

        if not re.match(id_pattern,outstudentid):
            errors.append('Invalid Student ID e.g. (CO202100123)')

        if student:
            if course.students.filter(student_id = outstudentid).exists():
                course.students.remove(student)
                return redirect('courseattendance', course_id=course_id)
            else:
                errors.append('Student is already not enrolled in the subject')
        else:
            errors.append('Student does not exist')

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('deletestudent', course_id=course_id)

    return render(request, "adminapp/deletestudent.html",{'course': course})

def is_valid_email(email):
    # Regular expression pattern for validating email
    email_regex = r'^[a-zA-Z0-9_.+-]+@gbox.adnu.edu.ph'

    if re.match(email_regex, email):
        return True
    else:
        return False

def role_redirect(request):
    if request.method == "POST":
        outusertype = request.POST['inusertype'];
        if outusertype == "student":
            return redirect(reverse('instudent'))
        elif outusertype == "teacher":
            return redirect(reverse('inteacher'))
        elif outusertype == "admin":
            return redirect(reverse('inadmin'))
    return redirect('index')



