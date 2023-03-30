import os

import psycopg2
from postgres_tasks.celery import app
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
