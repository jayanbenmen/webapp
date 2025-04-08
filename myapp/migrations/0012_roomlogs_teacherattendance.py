# Generated by Django 5.1.4 on 2025-03-16 12:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_studentattendance'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_date', models.DateField()),
                ('time_log', models.TimeField()),
                ('status', models.CharField(max_length=5)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.rooms')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.students')),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.teachers')),
            ],
            options={
                'db_table': 'room_logs',
            },
        ),
        migrations.CreateModel(
            name='TeacherAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_date', models.DateField()),
                ('time_in', models.TimeField()),
                ('time_out', models.TimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=10, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.courses')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.rooms')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.teachers')),
            ],
            options={
                'db_table': 'teacher_attendance',
                'unique_together': {('day_date', 'teacher', 'course')},
            },
        ),
    ]
