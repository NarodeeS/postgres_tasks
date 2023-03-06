from postgres_tasks.celery import app
from django.conf import settings
from psycopg2 import connect
from .models import DatabaseInfo
from .utils.database_status import DatabaseStatus


@app.task
def create_db() -> None:
    db_name = 'test_db' # generate based in username and task_name
    db_info = DatabaseInfo.objects.create(db_name=db_name)
    connection = connect(settings.SANDBOX_CONNECTION_STRING)

    with connection.cursor() as cursor:
        command = f'CREATE DATABASE {db_name};'
        try:
            cursor.execute(command)
        except Exception:
            db_info.status = DatabaseStatus.ERROR.value
            db_info.save()
            return

        # fill database for particular task
        
        db_info.status = DatabaseStatus.UP.value
        db_info.save()


@app.task
def delete_db(db_name: str) -> None:
    db_info = DatabaseInfo.objects.get(db_name=db_name)
    connection = connect(settings.SANDBOX_CONNECTION_STRING)
    
    with connection.cursor() as cursor:
        command = f'DROP DATABASE {db_name};'
        try:
            cursor.execute(command)
            db_info.delete()
        except Exception:
            db_info.status = DatabaseStatus.ERROR.value
            db_info.save()
