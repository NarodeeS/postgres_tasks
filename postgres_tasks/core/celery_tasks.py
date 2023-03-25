import os

import psycopg2
from postgres_tasks.celery import app
from .models import DatabaseInfo
from .service.database_status import DatabaseStatus
from .utils.get_database_connection import get_admin_connection
from .service.fill_task_db import fill_task_db
from .service.utils.get_db_info import get_db_info
from .service.utils.get_user_task import get_user_task
from .utils.connection_manager import ConnectionManager


@app.task
def create_db(user_task_id: int, db_name: str) -> None:
    user_task = get_user_task(user_task_id)
    user = user_task.user
    db_username = user.username
    db_password = user.password[:10]
    
    admin_db_name: str = os.getenv('POSTGRES_DB')  # type: ignore
    
    with ConnectionManager(get_admin_connection(admin_db_name)) as connection:
        with connection.cursor() as cursor:
            db_info = DatabaseInfo.objects.create(db_name=db_name, 
                                                  db_password=db_password,
                                                  user_task=user_task)
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
    db_username = db_info.get_user().username
    
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
