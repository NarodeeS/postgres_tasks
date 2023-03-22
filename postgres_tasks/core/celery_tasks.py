import os

import psycopg2
from postgres_tasks.celery import app
from .models import DatabaseInfo, UserTask
from .service.database_status import DatabaseStatus
from .utils.get_database_connection import get_admin_connection
from .service.fill_task_db import fill_task_db
from .utils.connection_manager import ConnectionManager


@app.task
def create_db(db_name: str, task_name: str) -> None:
    #  later get credentials based on User model
    username = 'test_user'
    password = 'test_password'
    admin_db_name: str = os.getenv('POSTGRES_DB')  # type: ignore
    
    user_task = (UserTask.objects.filter(active_task__task__title=task_name)
                                 .first())
    
    with ConnectionManager(get_admin_connection(admin_db_name)) as connection:
        with connection.cursor() as cursor:
            db_info = DatabaseInfo.objects.create(db_name=db_name, 
                                                  user_task=user_task)
            command = f'CREATE DATABASE {db_name};'
            try:
                cursor.execute(command)     
            except psycopg2.Error as err:
                print(err.pgerror)
                db_info.status = DatabaseStatus.ERROR.value
                db_info.save()
                return
    
    fill_task_db(db_name, username, password)


@app.task
def delete_db(db_name: str) -> None:
    db_info = DatabaseInfo.objects.get(db_name=db_name)
    admin_db_name: str = os.getenv('POSTGRES_DB')  # type: ignore
    username = 'test_user'  # get from db_info
    
    with ConnectionManager(get_admin_connection(admin_db_name)) as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(f'DROP DATABASE {db_name};')
                cursor.execute(f'DROP ROLE {username};')
                db_info.delete()
            except psycopg2.Error as err:
                print(err.pgerror)                
                db_info.status = DatabaseStatus.ERROR.value
                db_info.save()
