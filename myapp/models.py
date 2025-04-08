from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Users(models.Model):
    user_id = models.AutoField(primary_key = True, null = False)
    email = models.EmailField(null = False)
    pw = models.CharField(max_length = 128, null = False)
    user_type = models.CharField(max_length = 50, null = False)
    au_user = models.OneToOneField(User, on_delete=models.CASCADE, blank = True, null = True, related_name="custom_user")

    class Meta:
        db_table = "users"

class Students(models.Model):
    student_id = models.CharField(max_length = 50, primary_key=True, null = False)
    user = models.ForeignKey(Users, on_delete = models.CASCADE, null = False)
    first_name = models.CharField(max_length = 50, null = False)
    last_name = models.CharField(max_length=50, null = False)
    nfc_uid = models.CharField(max_length=50, null = True, blank=True)
    courses = models.ManyToManyField('Courses', related_name = 'students')
    au_user = models.OneToOneField(User, on_delete=models.CASCADE, blank = True, null = True, related_name="custom_student")

    class Meta:
        db_table = "students"

class Teachers(models.Model):
    teacher_id = models.CharField(max_length = 50, primary_key=True, null = False)
    user = models.ForeignKey(Users, on_delete = models.CASCADE, null = False)
    first_name = models.CharField(max_length = 50, null = False)
    last_name = models.CharField(max_length=50, null = False)
    nfc_uid = models.CharField(max_length=50, null = True, blank=True)
    au_user = models.OneToOneField(User, on_delete=models.CASCADE, blank = True, null = True, related_name="custom_teacher")

    class Meta:
        db_table = "teachers"

class Admins(models.Model):
    admin_id = models.AutoField(primary_key = True, null = False)
    username = models.CharField(max_length = 50, null = False)
    user = models.ForeignKey(Users, on_delete = models.CASCADE, null = False)
    first_name = models.CharField(max_length = 50, null = False)
    last_name = models.CharField(max_length=50, null = False)
    au_user = models.OneToOneField(User, on_delete=models.CASCADE, blank = True, null = True, related_name="custom_admin")

    class Meta:
        db_table = "admins"

class Rooms(models.Model):
    room_id = models.AutoField(primary_key = True, null = False)
    room_name = models.CharField(max_length = 50, null = False)

    class Meta:
        db_table = "rooms"

class Courses(models.Model):
    course_id = models.AutoField(primary_key = True, null = False)
    course_code = models.CharField(max_length = 50, null = False)
    course_title = models.CharField(max_length=50, null=False)
    section = models.CharField(max_length=50, null=False)
    start_time = models.TimeField()
    end_time = models.TimeField()
    schedule_day = models.CharField(max_length = 3, null = False)
    teacher = models.ForeignKey(Teachers, on_delete = models.CASCADE, null = False)
    room = models.ForeignKey(Rooms, on_delete = models.CASCADE, null = False)

    class Meta:
        db_table = "courses"

class Asynchs(models.Model):
    course = models.ForeignKey(Courses, on_delete = models.CASCADE, related_name = "asynchs", null = False)
    date = models.DateField()

    class Meta:
        db_table = "asynchs"

class StudentAttendance(models.Model):
    day_date = models.DateField()
    student = models.ForeignKey(Students, on_delete = models.CASCADE, null = False)
    course = models.ForeignKey(Courses, on_delete = models.CASCADE, null = False)
    room = models.ForeignKey(Rooms, on_delete = models.CASCADE, null = False)
    time_in = models.TimeField()
    time_out = models.TimeField(null = True, blank = True)
    status = models.CharField(max_length = 10, null = True, blank = True)
    is_synced = models.BooleanField(default = False, blank = False)
    
    class Meta:
        db_table = "student_attendance"
        unique_together = ("day_date", "student", "course")

class ManualAttendance(models.Model):
    day_date = models.DateField()
    student = models.ForeignKey(Students, on_delete = models.CASCADE, null = False)
    course = models.ForeignKey(Courses, on_delete = models.CASCADE, null = False)
    room = models.ForeignKey(Rooms, on_delete = models.CASCADE, null = False)
    time_in = models.TimeField()
    time_out = models.TimeField(null = True, blank = True)
    status = models.CharField(max_length = 10, null = True, blank = True)
    is_synced = models.BooleanField(default = False, blank = False)

    class Meta:
        db_table = "manual_attendance"
        unique_together = ("day_date", "student", "course")

class TeacherAttendance(models.Model):
    day_date = models.DateField()
    teacher = models.ForeignKey(Teachers, on_delete = models.CASCADE, null = False)
    course = models.ForeignKey(Courses, on_delete = models.CASCADE, null = False)
    room = models.ForeignKey(Rooms, on_delete = models.CASCADE, null = False)
    time_in = models.TimeField()
    time_out = models.TimeField(null = True, blank = True)
    status = models.CharField(max_length = 10, null = True, blank = True)
    is_synced = models.BooleanField(default = False, blank = False)

    class Meta:
        db_table = "teacher_attendance"
        unique_together = ("day_date", "teacher", "course")

class RoomLogs(models.Model):
    day_date = models.DateField()
    time_log = models.TimeField()
    room = models.ForeignKey(Rooms, on_delete = models.CASCADE, null = False)
    student = models.ForeignKey(Students, on_delete = models.CASCADE, null = True, blank = True)
    teacher = models.ForeignKey(Teachers, on_delete = models.CASCADE, null = True, blank = True)
    status = models.CharField(max_length = 5, null = False)
    is_synced = models.BooleanField(default = False, blank = False)

    class Meta:
        db_table = "room_logs"

@receiver(post_save, sender = User)
def update_users(sender, instance, **kwargs):
    if hasattr(instance, "custom_user"):
        instance.custom_user.email = instance.email
        instance.custom_user.pw = instance.password
        instance.custom_user.save()

@receiver(post_save, sender = User)
def update_students(sender, instance, **kwargs):
    if hasattr(instance, "custom_student"):
        instance.custom_student.first_name = instance.first_name
        instance.custom_student.last_name = instance.last_name
        instance.custom_student.save()

@receiver(post_save, sender = User)
def update_teachers(sender, instance, **kwargs):
    if hasattr(instance, "custom_teacher"):
        instance.custom_teacher.first_name = instance.first_name
        instance.custom_teacher.last_name = instance.last_name
        instance.custom_teacher.save()

@receiver(post_save, sender = User)
def update_admins(sender, instance, **kwargs):
    if hasattr(instance, "custom_admin"):
        instance.custom_admin.first_name = instance.first_name
        instance.custom_admin.last_name = instance.last_name
        instance.custom_admin.save()
