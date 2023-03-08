import os

import psycopg2
from postgres_tasks.celery import app
from .models import DatabaseInfo
from .utils.database_status import DatabaseStatus
from .utils.get_database_connection import get_admin_connection
from .utils.fill_db import fill_db
from .utils.connection_manager import ConnectionManager


@app.task
def create_db(db_name: str) -> None:
    #  later get credentials bases on User model
    username = 'test_user'
    password = 'test_password'
    admin_db_name = os.getenv('POSTGRES_DB')
    
    with ConnectionManager(get_admin_connection(admin_db_name)) as connection:
        with connection.cursor() as cursor:
            db_info = DatabaseInfo.objects.create(db_name=db_name)
            command = f'CREATE DATABASE {db_name};'
            try:
                cursor.execute(command)     
            except psycopg2.Error as err:
                print(err.pgerror)
                db_info.status = DatabaseStatus.ERROR.value
                db_info.save()
                return
    
    fill_db(db_name, username, password)


@app.task
def delete_db(db_name: str) -> None:
    db_info = DatabaseInfo.objects.get(db_name=db_name)
    admin_db_name = os.getenv('POSTGRES_DB')
    username = 'test_user'  # get from db
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
