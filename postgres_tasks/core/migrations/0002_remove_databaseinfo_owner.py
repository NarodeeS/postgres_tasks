# Generated by Django 4.1.7 on 2023-03-06 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='databaseinfo',
            name='owner',
        ),
    ]
