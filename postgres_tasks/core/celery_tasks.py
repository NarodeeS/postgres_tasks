import os

import psycopg2
import postgres_tasks.settings as settings
from random import randrange
from postgres_tasks.celery import app
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from socket import gaierror
from django.core.cache import cache

from .models import DatabaseInfo, User, Task
from .service.database_status import DatabaseStatus
from .utils.get_database_connection import get_admin_connection
from .service.fill_task_db import fill_task_db
from .service.utils.get_db_info import get_db_info
from .utils.connection_manager import ConnectionManager


@app.task
def create_db(user_id: int, task_id: int, db_name: str) -> None:
    user: User = User.objects.filter(id=user_id).first() # type: ignore
    db_username = user.get_db_username()
    db_password = user.password[:10]
    task: Task = Task.objects.filter(id=task_id).first() # type: ignore
    
    admin_db_name: str = os.getenv('POSTGRES_DB')  # type: ignore
    
    with ConnectionManager(get_admin_connection(admin_db_name)) as connection:
        with connection.cursor() as cursor:
            db_info = DatabaseInfo.objects.create(db_name=db_name, 
                                                  db_password=db_password,
                                                  task=task,
                                                  user=user)
            command = f'CREATE DATABASE {db_name};'
            try:
                cursor.execute(command)     
            except psycopg2.Error as err:
                print(err.pgerror)
                db_info.status = DatabaseStatus.ERROR.value
                db_info.save()
                return
    
    fill_task_db(db_name, db_username, db_password)


@app.task
def delete_db(db_name: str) -> None:
    db_info = get_db_info(db_name)
    db_username = db_info.user.get_db_username()
    
    admin_db_name: str = os.getenv('POSTGRES_DB')  # type: ignore
    
    with ConnectionManager(get_admin_connection(admin_db_name)) as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(f'DROP DATABASE {db_name};')
                cursor.execute(f'DROP ROLE {db_username};')
                db_info.delete()
            except psycopg2.Error as err:
                print(err.pgerror)                
                db_info.status = DatabaseStatus.ERROR.value
                db_info.save()


@app.task
def send_verification_email(email: str) -> None:
    number_for_verification = randrange(1000, 9999)
    cache.set(email, number_for_verification, 60000)

    msg_html = render_to_string('core/email_template.html', {'number_for_verification': number_for_verification})

    send_mail(
        "Subject here",
        "Here is the message.",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
        html_message=msg_html,
    )
