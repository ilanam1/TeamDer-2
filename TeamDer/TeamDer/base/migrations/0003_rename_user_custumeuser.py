# Generated by Django 5.0.3 on 2024-03-31 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_loginuser_alter_user_birth_day'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='custumeUser',
        ),
    ]
