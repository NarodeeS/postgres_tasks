from datetime import datetime

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.cache import cache
import psycopg2
from random import randrange

from config import SANDBOX_POSTGRES_DB, DATABASE_INFO_LIFETIME
from core.models import DatabaseInfo, User, Task, CompletedTask
from core.utils.db_utils import get_admin_connection
from .database_status import DatabaseStatus
from .errors import NoSuchDbError
from .fill_task_db import fill_task_db, DbConnectionManager
from postgres_tasks.celery import app
import postgres_tasks.settings as settings
from .service_utils import get_db_info


@app.task
def create_db_task(user_id: int, task_id: int, db_name: str) -> None:
    user: User = User.objects.filter(id=user_id).first() # type: ignore
    db_username = user.get_db_username()
    db_password = user.password[:10]
    task: Task = Task.objects.filter(id=task_id).first() # type: ignore
    
    admin_db_name: str = SANDBOX_POSTGRES_DB
    
    with DbConnectionManager(get_admin_connection(admin_db_name)) as connection:
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
def delete_db_task(db_name: str) -> None:
    db_info = get_db_info(db_name)
    db_username = db_info.user.get_db_username()
    
    admin_db_name: str = SANDBOX_POSTGRES_DB
    
    with DbConnectionManager(get_admin_connection(admin_db_name)) as connection:
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
def send_verification_email_task(email: str) -> None:
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


@app.task
def clean_inactive_databases_task() -> None:
    all_databases = DatabaseInfo.objects.all()
    for database in all_databases:
        date_diff = datetime.now() - database.last_action_datetime
        if date_diff.total_seconds() >= DATABASE_INFO_LIFETIME:
            delete_db_task(database.db_name)


def delete_db(db_name: str):
    database_info = (DatabaseInfo.objects
                                 .filter(db_name=db_name)
                                 .first())
    if not database_info:
        raise NoSuchDbError(db_name)
    delete_db_task.delay(db_name)


def finish_task(db_name: str):
    '''
    Create 'CompletedTask' and delete db for this task
    '''
    db_info = get_db_info(db_name)
    potential_completed_task = (CompletedTask.objects
                                             .filter(task__id=db_info.task.id, 
                                                     user__id=db_info.user.id))
    if not potential_completed_task:
        CompletedTask.objects.create(task=db_info.task, 
                                     user=db_info.user)
    delete_db_task.delay(db_name)
