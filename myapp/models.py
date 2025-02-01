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

    class Meta:
        db_table = "students"

class Teachers(models.Model):
    teacher_id = models.CharField(max_length = 50, primary_key=True, null = False)
    user = models.ForeignKey(Users, on_delete = models.CASCADE, null = False)
    first_name = models.CharField(max_length = 50, null = False)
    last_name = models.CharField(max_length=50, null = False)
    nfc_uid = models.CharField(max_length=50, null = True, blank=True)

    class Meta:
        db_table = "teachers"

class Admins(models.Model):
    admin_id = models.AutoField(primary_key = True, null = False)
    username = models.CharField(max_length = 50, null = False)
    user = models.ForeignKey(Users, on_delete = models.CASCADE, null = False)
    first_name = models.CharField(max_length = 50, null = False)
    last_name = models.CharField(max_length=50, null = False)

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
        

@receiver(post_save, sender = User)
def update_users(sender, instance, **kwargs):
    if hasattr(instance, "custom_user"):
        instance.custom_user.pw = instance.password
        instance.custom_user.save()
