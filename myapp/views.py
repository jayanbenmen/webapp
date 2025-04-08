from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.core.paginator import Paginator

from .decorators import unauthenticated_user, allowed_users
from .models import Users
from .models import Students
from .models import Teachers
from .models import Admins
from .models import Rooms
from .models import Courses
from .models import StudentAttendance
from .models import TeacherAttendance
from .models import RoomLogs
from .models import ManualAttendance
from django.db import transaction
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from .forms import AdminCreationForm
from .forms import PasswordChangingForm
from .forms import CalendarForm
from .forms import DateForm
from django.middleware.csrf import get_token
import re
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from datetime import datetime
from calendar import monthrange
import csv


# Create your views here.

def index(request):
    return render(request, "myapp/index.html", {})

def initial(request):
    return render(request, "myapp/initial.html", {})

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
        outnfcuid = request.POST.get('innfcuid').strip()
        outusertype = "student"

        errors = []
        id_pattern = r'^CO20\d{7}$'

        if outstudentid == '' or outfirstname == '' or outlastname == '' or outemail == '' or outpw1 == '' or outpw2 == '' or outnfcuid == '':
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

        if len(outnfcuid) != 8:
            errors.append('Invalid NFC pattern')

        if not re.fullmatch(r'[0-9A-Fa-f]+', outnfcuid):
            errors.append('Only hexadecimal characters (0-9, A-F) are allowed')

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('instudent')
        
        outnfcuid = outnfcuid.upper()
        outnfcuid = ":".join(outnfcuid[i:i+2] for i in range(0, 8, 2))

        messages.success(request, 'Account was created for  ' + outstudentid)
        au = User.objects.create_user(username=outstudentid,first_name = outfirstname, last_name = outlastname, email=outemail, password=outpw1)
        au.save()

        group = Group.objects.get(name='student')
        au.groups.add(group)

        us = Users(email = outemail, pw = outpw1, user_type = outusertype, au_user_id = au.id)
        us.save()
        outuserid = us.user_id
        st = Students(student_id=outstudentid, user_id=outuserid, first_name=outfirstname, last_name=outlastname, nfc_uid=outnfcuid, au_user_id = au.id)
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

        if outteacherid == '' or outfirstname == '' or outlastname == '' or outemail == '' or outpw1 == '' or outpw2 == '' or outnfcuid == '':
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

        if len(outnfcuid) != 8:
            errors.append('Invalid NFC pattern')

        if not re.fullmatch(r'[0-9A-Fa-f]+', outnfcuid):
            errors.append('Only hexadecimal characters (0-9, A-F) are allowed')

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('inteacher')
        
        outnfcuid = outnfcuid.upper()
        outnfcuid = ":".join(outnfcuid[i:i+2] for i in range(0, 8, 2))

        messages.success(request, 'Account was created for  ' + outteacherid)
        au = User.objects.create_user(username=outteacherid,first_name = outfirstname, last_name = outlastname, email=outemail, password=outpw1)
        au.save()

        group = Group.objects.get(name='teacher')
        au.groups.add(group)

        us = Users(email=outemail, pw=outpw1, user_type=outusertype, au_user_id=au.id)
        us.save()
        outuserid = us.user_id
        te = Teachers(teacher_id=outteacherid, user_id=outuserid, first_name=outfirstname, last_name=outlastname, nfc_uid=outnfcuid, au_user_id = au.id)
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
        ad = Admins(username=outusername, user_id=outuserid, first_name=outfirstname, last_name=outlastname, au_user_id = su.id)
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
                 return redirect('admincourses')

         else:
             messages.info(request, 'ID Number or Password is Incorrect')
             return render(request, "myapp/index.html", {})

    return render(request, "myapp/index.html", {})

def logoutUser(request):
    logout(request)
    return redirect('login')

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    def get_success_url(self):
        user = self.request.user  
        messages.success(self.request, 'Your password has been successfully changed!')
        if user.groups.filter(name='student').exists():
            return reverse_lazy('student_profile')  
        else:
            return reverse_lazy('teacher_profile')
          
def password_success(request):
    return render(request, 'registration/password_success.html', {})

def goto_profile(request):
    user = request.user

    if user.groups.filter(name='student').exists():
        return redirect('student_profile')
    elif user.groups.filter(name='teacher_profile').exists():
        return redirect('teacherhome')

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['student'])
def student_profile(request):
    student = Students.objects.filter(user_id = request.user.id).first()
    return render(request, 'studentapp/student_profile.html', {'student': student})   

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['student'])
def student_courses(request):
    student = Students.objects.filter(user_id = request.user.id).first()
    courses = student.courses.all()
    return render(request, 'studentapp/student_courses.html', {'courses': courses}) 

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['student'])
def attendance(request, course_id):
    course = get_object_or_404(Courses.objects.select_related('teacher', 'room'), course_id=course_id)
    student = Students.objects.filter(user_id = request.user.id).first()
    records = StudentAttendance.objects.filter(student=student, course=course).select_related('student', 'course', 'room')
    return render(request, "studentapp/attendance.html",{'course': course, 'teacher': course.teacher, 'room': course.room, 'records': records})

def student_nfcupd(request):
    student = Students.objects.filter(user_id = request.user.id).first()

    if request.method == "POST":
        errors = []
        outstudentnfc = request.POST.get('instudentnfc').strip()

        if len(outstudentnfc) != 8:
            errors.append('Invalid Input')

        if not re.fullmatch(r'[0-9A-Fa-f]+', outstudentnfc):
            errors.append('Only hexadecimal characters (0-9, A-F) are allowed')

        outstudentnfc = outstudentnfc.upper()

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('student_nfcupd')
                
        student.nfc_uid = ":".join(outstudentnfc[i:i+2] for i in range(0, 8, 2))  # Format as XX:XX:XX:XX
        student.save()
        return redirect('student_profile')
    return render(request, "studentapp/student_nfcupd.html",{'student': student})

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['teacher'])
def teacher_profile(request):
    teacher = Teachers.objects.filter(user_id = request.user.id).first()
    return render(request, 'teacherapp/teacher_profile.html', {'teacher': teacher})     

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['teacher'])
def teacher_courses(request):
    teacher = Teachers.objects.filter(user_id = request.user.id).first()
    courses = Courses.objects.filter(teacher = teacher)
    return render(request, 'teacherapp/teacher_courses.html', {'courses': courses})      

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['teacher'])
def studentattendance(request, course_id):
    course = get_object_or_404(Courses.objects.select_related('teacher', 'room'), course_id=course_id)
    students = course.students.all()
    date = datetime.now().date()
    form = DateForm(request.POST or None, initial={'day_date': date})

    if form.is_valid():
        date = form.cleaned_data['day_date']

    attendance_records = StudentAttendance.objects.filter(course = course, day_date = date)

    attendance_dict = {record.student_id: record for record in attendance_records}

    for student in students:
        student.attendance = attendance_dict.get(student.student_id, None)

    return render(request, "teacherapp/studentattendance.html", {'course': course, 'teacher': course.teacher, 'room': course.room, 'students': students, 'form': form})


@login_required(login_url = 'login')
@allowed_users(allowed_roles=['teacher'])
def teacherattendance(request, course_id):
    course = get_object_or_404(Courses.objects.select_related('teacher', 'room'), course_id=course_id)
    teacher = Teachers.objects.filter(user_id = request.user.id).first()
    records = TeacherAttendance.objects.filter(teacher=teacher, course=course).select_related('teacher', 'course', 'room')
    return render(request, "teacherapp/teacherattendance.html",{'course': course, 'teacher': course.teacher, 'room': course.room, 'records': records})

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['teacher'])
def teacher_classlist(request, course_id):
    course = get_object_or_404(Courses.objects.select_related('teacher', 'room').prefetch_related('students'),course_id=course_id)
    students = course.students.all()
    return render(request, "teacherapp/teacher_classlist.html",{'course': course, 'teacher': course.teacher, 'room': course.room, 'students': students})

def teacher_nfcupd(request):
    teacher = Teachers.objects.filter(user_id = request.user.id).first()

    if request.method == "POST":
        errors = []
        outteachernfc = request.POST.get('inteachernfc').strip()

        if len(outteachernfc) != 8:
            errors.append('Invalid Input')

        if not re.fullmatch(r'[0-9A-Fa-f]+', outteachernfc):
            errors.append('Only hexadecimal characters (0-9, A-F) are allowed')

        outteachernfc = outteachernfc.upper()

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('teacher_nfcupd')
                
        teacher.nfc_uid = ":".join(outteachernfc[i:i+2] for i in range(0, 8, 2))  # Format as XX:XX:XX:XX
        teacher.save()
        return redirect('teacher_profile')
    return render(request, "teacherapp/teacher_nfcupd.html",{'teacher': teacher})

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['teacher'])
def manual_attendance(request, course_id):
    course = get_object_or_404(Courses.objects.select_related('teacher', 'room'), course_id=course_id)
    students = course.students.all()
    current_datetime = datetime.now()
    current_date = current_datetime.date()
    current_time = current_datetime.time()
    current_day = current_datetime.strftime('%A')
    end_time = course.end_time

    day_mapping = {
        "Monday": ["MON", "MW"],
        "Tuesday": ["TUE", "TTH"],
        "Wednesday": ["WED", "MW"],
        "Thursday": ["THU", "TTH"],
        "Friday": ["FRI", "FSA"],
        "Saturday": ["SAT", "FSA"],
        "Sunday": ["SUN"]
    }

    if request.method == "POST":
        errors = []    
        outstudentid = request.POST.get('instudentid')
        outstatus = request.POST.get('instatus')
        if course.schedule_day in day_mapping[current_day]:
            if course.start_time <= current_time <= course.end_time:
                attendance_exists = StudentAttendance.objects.filter(day_date = current_date, student_id = outstudentid, course_id = course.course_id)
                if attendance_exists:
                    errors.append('Attendance for student already exists')
                else:
                    ma = ManualAttendance(day_date = current_date, time_in = current_time, time_out = end_time, status = outstatus, course_id = course.course_id, room_id = course.room_id, student_id = outstudentid, is_synced = 1)
                    sa = StudentAttendance(day_date = current_date, time_in = current_time, time_out = end_time, status = outstatus, course_id = course.course_id, room_id = course.room_id, student_id = outstudentid, is_synced = 1)
                    ma.save()
                    sa.save()
            else:
                errors.append('Must record attendance during class hours only')
        else:
            errors.append('Must record attendance during scheduled days only')

        if errors:
            for error in errors:
                messages.error(request, error)
            
        return redirect('manual_attendance', course.course_id)

    return render(request, "teacherapp/manual_attendance.html",{'course': course, 'students': students, 'current_date': current_date})

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['student'])
def studenthome(request):
    student = Students.objects.filter(user_id=request.user.id).first()
    if not student:
        # Handle case where student is not found
        return render(request, "studentapp/studenthome.html", {'error': 'Student not found'})

    form = CalendarForm(request.POST or None)
    courses = student.courses.all()
    attendance_data = []

    month = datetime.now().month
    year = datetime.now().year

    if form.is_valid():
        month = int(form.cleaned_data['month'])
    
    _, num_days = monthrange(year, month)

    # Generate the list of all dates for the current month
    dates = [datetime(year, month, day) for day in range(1, num_days + 1)]
    formatted_dates = [date.strftime('%Y-%m-%d') for date in dates]

    # Pre-fetch all the attendance records in one query
    attendance_records = StudentAttendance.objects.filter(
        student=student,
        course__in=courses,
        day_date__in=formatted_dates
    )

    # Create a dictionary to map attendance data by (course_id, date)
    attendance_dict = {}
    for record in attendance_records:
        attendance_dict[(record.course.course_id, record.day_date.strftime('%Y-%m-%d'))] = record.status

    # Populate the attendance_data list by iterating over courses and dates
    for course in courses:
        for date in formatted_dates:
            status = attendance_dict.get((course.course_id, date), "")
            if status == "On Time":
                status = "✔"
            elif status == "Late":
                status = "L"
            elif status == "Absent":
                status = "A"
            # Add the attendance data to the list
            attendance_data.append({
                'course_id': course.course_id,
                'date': date,
                'status': status
            })
    
    return render(request, "studentapp/studenthome.html", {
        'student': student,
        'courses': courses,
        'form': form,
        'dates': dates,
        'attendance_data': attendance_data
    })

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['teacher'])
def teacherhome(request):
    # Get teacher object directly without redundant queries
    teacher = Teachers.objects.filter(user_id=request.user.id).first()
    if not teacher:
        # Handle the case where the teacher is not found (optional)
        return render(request, "teacherapp/teacherhome.html", {'error': 'Teacher not found'})

    form = CalendarForm(request.POST or None)
    courses = Courses.objects.filter(teacher_id=teacher.teacher_id)
    attendance_data = []

    # Default to current month and year
    month = datetime.now().month
    year = datetime.now().year

    if form.is_valid():
        month = int(form.cleaned_data['month'])
    
    _, num_days = monthrange(year, month)

    # Generate dates and formatted_dates for the month
    dates = [datetime(year, month, day) for day in range(1, num_days + 1)]
    formatted_dates = [date.strftime('%Y-%m-%d') for date in dates]

    # Pre-fetch all teacher attendance records in one query
    attendance_records = TeacherAttendance.objects.filter(
        teacher=teacher,
        course__in=courses,
        day_date__in=formatted_dates
    )

    # Create a dictionary to store attendance by (course_id, date)
    attendance_dict = {}
    for record in attendance_records:
        attendance_dict[(record.course.course_id, record.day_date.strftime('%Y-%m-%d'))] = record.status

    # Populate the attendance_data list
    for course in courses:
        for date in formatted_dates:
            status = attendance_dict.get((course.course_id, date), "")
            if status == "On Time":
                status = "✔"
            elif status == "Late":
                status = "L"
            elif status == "Absent":
                status = "A"
            # Add attendance data for this course and date to the list
            attendance_data.append({
                'course_id': course.course_id,
                'date': date,
                'status': status
            })

    return render(request, "teacherapp/teacherhome.html", {
        'teacher': teacher,
        'courses': courses,
        'form': form,
        'dates': dates,
        'attendance_data': attendance_data
    })

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
    date = datetime.now().date()
    form = DateForm(request.POST or None, initial={'day_date': date})

    if form.is_valid():
        date = form.cleaned_data['day_date']

    log_records = RoomLogs.objects.filter(room = room, day_date = date).order_by('day_date', 'time_log')

    return render(request, "adminapp/roomattendance.html",{'room': room, 'log_records': log_records, 'form': form, 'date': date})

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
            return HttpResponse()
    return render(request, "adminapp/addroom.html",{})

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def deleteroom(request):
    rooms = Rooms.objects.all()
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
    return render(request, "adminapp/deleteroom.html",{'rooms': rooms})

def deleteroombutton(request,room_id):
    room = Rooms.objects.get(room_id = room_id)
    room.delete()
    return redirect("adminrooms")

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def admincourses(request):
    courses = Courses.objects.all()
    courses = Courses.objects.select_related('teacher').all()
    return render(request, "adminapp/courses.html",{'courses': courses})

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def courseattendance(request, course_id):
    course = get_object_or_404(Courses.objects.select_related('teacher', 'room'), course_id=course_id)
    students = course.students.all()
    date = datetime.now().date()
    form = DateForm(request.POST or None, initial={'day_date': date})

    if form.is_valid():
        date = form.cleaned_data['day_date']

    student_attendance_records = StudentAttendance.objects.filter(course = course, day_date = date)
    teacher_attendance_records = TeacherAttendance.objects.filter(course = course, day_date  = date)

    attendance_dict = {record.student_id: record for record in student_attendance_records}

    for student in students:
        student.attendance = attendance_dict.get(student.student_id, None)
    return render(request, "adminapp/courseattendance.html",{'course': course, 'teacher': course.teacher, 'room': course.room, 'students': students, 'form': form, 'teacher_records': teacher_attendance_records})

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

            if outcoursecode == '' or outcoursetitle == '' or outsection == '' or outstarttime == '' or outendtime == '' or outday == '' or outroom == '' or outteacherid == '':
                errors.append('Missing required fields')

            room = Rooms.objects.filter(room_name=outroom).first()
            if not room:
                 errors.append(f"Room does not exist")

            if room:
                sched_conflict = Courses.objects.filter(
                    room_id = room.room_id,
                    schedule_day = outday
                ).filter(
                    start_time__lt=outendtime,  
                    end_time__gt=outstarttime  
                ).exists()
                if sched_conflict:
                    errors.append('Conflict with existing courses in the same room')


            subj_conflict = Courses.objects.filter(
                course_code = outcoursecode,
                section = outsection
            ).exists()
            if subj_conflict:
                errors.append('Course and Section already exists')

            teacher_exists = Teachers.objects.filter(teacher_id=outteacherid).exists()
            if not teacher_exists:
                errors.append('Teacher does not exist')

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
            return HttpResponse()

    return render(request, "adminapp/addcourse.html",{})

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def deletecourse(request):
    courses = Courses.objects.all()
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

    return render(request, "adminapp/deletecourse.html", {'courses':courses})

def deletecoursebutton(request,course_id):
    course = Courses.objects.get(course_id = course_id)
    course.delete()
    return redirect("admincourses")

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def addstudent(request, course_id):
    course = get_object_or_404(Courses, course_id=course_id)
    unenrolled_students = Students.objects.exclude(student_id__in=course.students.values_list('student_id', flat=True))
    if request.method == "POST":
        outstudentids= request.POST.getlist('instudentid')

        for outstudentid in outstudentids:
            student = get_object_or_404(Students, student_id=outstudentid)
            student.courses.add(course)
        return redirect("adminstudentlist", course_id = course_id)

    return render(request, "adminapp/addstudent.html",{'course': course, 'unenrolled_students': unenrolled_students})

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def deletestudent(request, course_id):
    course = get_object_or_404(Courses, course_id=course_id)
    enrolled_students = Students.objects.filter(student_id__in=course.students.values_list('student_id', flat=True))

    if request.method == "POST":
        outstudentids= request.POST.getlist('instudentid')

        for outstudentid in outstudentids:
            student = get_object_or_404(Students, student_id=outstudentid)
            student.courses.remove(course)
        return redirect("adminstudentlist", course_id = course_id)        
    return render(request, "adminapp/deletestudent.html",{'course': course, 'enrolled_students': enrolled_students})

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def adminstudentlist(request, course_id):
    course = get_object_or_404(Courses.objects.select_related('teacher', 'room').prefetch_related('students'),course_id=course_id)
    students = course.students.all()
    return render(request, "adminapp/adminstudentlist.html",{'course': course, 'teacher': course.teacher, 'room': course.room, 'students': students})

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def nfcuid(request):
    teachers = Teachers.objects.all()
    students = Students.objects.all()
    return render(request, "adminapp/nfcuid.html",{'teachers': teachers, 'students': students})

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def updteachernfc(request, teacher_id):
    teacher = get_object_or_404(Teachers, teacher_id = teacher_id)

    if request.method == "POST":
        errors = []
        outteachernfc = request.POST.get('inteachernfc').strip()

        if len(outteachernfc) != 8:
            errors.append('Invalid Input, must exactly be 8 alphanumeric characters')

        if not re.fullmatch(r'[0-9A-Fa-f]+', outteachernfc):
            errors.append('Only hexadecimal characters (0-9, A-F) are allowed')

        outteachernfc = outteachernfc.upper()

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('updteachernfc', teacher_id)
                
        teacher.nfc_uid = ":".join(outteachernfc[i:i+2] for i in range(0, 8, 2))  # Format as XX:XX:XX:XX
        teacher.save()
        return HttpResponse()
    return render(request, "adminapp/updteachernfc.html", {'teacher': teacher})

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def updstudentnfc(request, student_id):
    student = get_object_or_404(Students, student_id = student_id)

    if request.method == "POST":
        errors = []
        outstudentnfc = request.POST.get('instudentnfc').strip()

        if len(outstudentnfc) != 8:
            errors.append('Invalid Input')

        if not re.fullmatch(r'[0-9A-Fa-f]+', outstudentnfc):
            errors.append('Only hexadecimal characters (0-9, A-F) are allowed')

        outstudentnfc = outstudentnfc.upper()

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('updstudentnfc', student_id)
                
        student.nfc_uid = ":".join(outstudentnfc[i:i+2] for i in range(0, 8, 2))  # Format as XX:XX:XX:XX
        student.save()
        return HttpResponse()
    return render(request, "adminapp/updstudentnfc.html",{'student': student})

def assign_teacher(request, course_id):
    course = get_object_or_404(Courses, course_id = course_id)
    teachers = Teachers.objects.all()

    if request.method == 'POST':
        outteacherid = request.POST.get('inteacherid')
        teacher = Teachers.objects.get(teacher_id = outteacherid)
        course.teacher = teacher
        course.save()

        return redirect('courseattendance', course_id = course_id)

    return render(request, "adminapp/assign_teacher.html", {'course': course, 'teachers': teachers})

# CSV
def students_monthly_attendance(request, course_id):
    course = get_object_or_404(Courses, course_id=course_id)
    date = datetime.now().date()
    form = DateForm(request.GET or None, initial={'day_date': date})

    if form.is_valid():
        date = form.cleaned_data['day_date']

    month = date.month
    year = date.year

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{month}_{year}_{course.course_code}_{course.section}.csv"'

    monthly_records = StudentAttendance.objects.filter(course = course, day_date__month = month, day_date__year = year)

    writer = csv.writer(response)

    writer.writerow(['Date', 'Name', 'Time-in', 'Time-out', 'Status'])

    for record in monthly_records:
        full_name = f"{record.student.first_name} {record.student.last_name}"
        time_in_formatted = record.time_in.strftime('%H:%M:%S') if record.time_in else ''
        time_out_formatted = record.time_out.strftime('%H:%M:%S') if record.time_out else ''
        writer.writerow([record.day_date, full_name, time_in_formatted, time_out_formatted, record.status])

    return response

def monthly_room_logs(request, room_id):
    room = get_object_or_404(Rooms, room_id = room_id)
    date = datetime.now().date()
    form = DateForm(request.GET or None, initial={'day_date': date})

    if form.is_valid():
        date = form.cleaned_data['day_date']

    month = date.month
    year = date.year

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{month}_{year}_{room.room_name}_logs.csv"'

    monthly_records = RoomLogs.objects.filter(room = room, day_date__month = month, day_date__year = year)

    writer = csv.writer(response)

    writer.writerow(['Date', 'Name', 'Time', 'Status'])

    for record in monthly_records:
        if record.student:
            full_name = f"{record.student.first_name} {record.student.last_name}"
        elif record.teacher:
            full_name = f"{record.teacher.first_name} {record.teacher.last_name}"

        time_log_formatted = record.time_log.strftime('%H:%M:%S') if record.time_log else ''
        writer.writerow([record.day_date, full_name, time_log_formatted, record.status])

    return response

def is_valid_email(email):
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
    return redirect('initial')



