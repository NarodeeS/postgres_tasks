# Generated by Django 4.1.7 on 2023-04-16 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_databaseinfo_moves_performed_task_moves_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='databaseinfo',
            name='last_action_datetime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
