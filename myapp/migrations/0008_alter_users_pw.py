# Generated by Django 5.1.4 on 2025-02-01 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_alter_users_au_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='pw',
            field=models.CharField(max_length=128),
        ),
    ]
