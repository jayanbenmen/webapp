# Generated by Django 5.1.4 on 2025-01-29 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_admins'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('room_id', models.AutoField(primary_key=True, serialize=False)),
                ('room_name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'rooms',
            },
        ),
    ]
