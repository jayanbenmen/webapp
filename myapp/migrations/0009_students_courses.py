# Generated by Django 5.1.4 on 2025-02-01 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_alter_users_pw'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='courses',
            field=models.ManyToManyField(related_name='students', to='myapp.courses'),
        ),
    ]
