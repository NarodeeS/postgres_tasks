from typing import TypedDict

from psycopg2 import Error as SQLError

from config import SANDBOX_POSTGRES_DB0
from domain import commands, events, errors
from domain.database_status import DatabaseStatus
from core.models import Task, CompletedTask, DatabaseInfo, User
from core.utils.db_utils import (database_exists, 
                                 get_db_info, 
                                 get_database_connection,
                                 get_admin_connection,
                                 DbConnectionManager)
from core.utils.load_file import load_file


def create_user_task(command: commands.CreateUserTask, 
                     message_queue: list) -> str:
    task = Task.objects.filter(id=command.task_id).first()
    if not task:
        raise errors.NoSuchTaskError(task)
    
    db_name = f"{'_'.join(task.title.split(' ')).lower()}_{command.user_id}"
    if not (db_info := database_exists(command.user_id)):
        creds = create_db(command.user_id, task.id, db_name)
        message_queue.append(events.DbCreated(db_name, *creds))
    else:
        if db_info.task.id != command.task_id:
            raise errors.TaskAlreadyStartedError(db_info.task.id)
    return db_name


def finish_user_task(command: commands.FinishUserTask, 
                     message_queue: list):
    db_info = get_db_info(command.db_name)
    potential_completed_task = (CompletedTask.objects
                                             .filter(task__id=db_info.task.id, 
                                                     user__id=db_info.user.id))
    if not potential_completed_task:
        CompletedTask.objects.create(task=db_info.task, 
                                     user=db_info.user)
    
    message_queue.append(events.TaskDisposed(command.db_name))


def delete_user_task_db(command: commands.DeleteUserTaskDb, 
                        message_queue: list):
    db_info = (DatabaseInfo.objects
                                 .filter(db_name=command.db_name)
                                 .first())
    if not db_info:
        raise errors.NoSuchDbError(command.db_name)
    
    message_queue.append(events.TaskDisposed(command.db_name))


class QueryResult(TypedDict):
    status: str
    result: list | None
    columns: list[str] | None
    error_message: str | None
    moves_left: int 


def send_sql_command(command: commands.SendSqlCommand, 
                     message_queue: list) -> QueryResult:
    db_info = get_db_info(command.db_name)
    db_username =  db_info.user.get_db_username()
    db_password = db_info.db_password
    connection = get_database_connection(command.db_name, db_username, db_password)
    
    with DbConnectionManager(connection):
        with connection.cursor() as cursor:
            try:
                if db_info.moves_performed >= db_info.task.moves_count:
                    raise errors.OutOfMovesError()
                db_info.increment_moves()
                cursor.execute(command.query)
                result = cursor.fetchall()
                column_names = [descr_row[0] for descr_row in cursor.description]
            except SQLError as error:
                return QueryResult(status=cursor.statusmessage,
                                   result=None,
                                   columns=None,
                                   error_message=error.pgerror,
                                   moves_left=db_info.moves_left)
            
            return QueryResult(status=cursor.statusmessage, 
                               result=result, 
                               columns=column_names,
                               error_message=None,
                               moves_left=db_info.moves_left)
        

def check_task(command: commands.CheckTask, 
               message_queue: list) -> bool:
    db_info = get_db_info(command.db_name)    
    check_script = load_file(db_info.task.check_script.file)
    connection = get_admin_connection(command.db_name)
    
    with DbConnectionManager(connection):
        with connection.cursor() as cursor:
            cursor.execute(check_script)
            row = cursor.fetchone()
            if row:    
                success, *_ = row
                return bool(success)
            
            return False


def fill_task_db(event: events.DbCreated,
                 message_queue: list):
    db_info = get_db_info(event.db_name)
    username, password = event.username, event.password
        
    task = db_info.task
    filling_command = load_file(task.creation_script.file)
    
    user_creation_command = f'''
        CREATE ROLE {username} WITH LOGIN PASSWORD '{password}';
        GRANT ALL ON SCHEMA public TO {username};
        GRANT ALL ON All TABLES IN SCHEMA public TO {username};
        GRANT ALL ON All SEQUENCES IN SCHEMA public TO {username};
        GRANT ALL ON All FUNCTIONS IN SCHEMA public TO {username};
        GRANT ALL ON All PROCEDURES IN SCHEMA public TO {username};
        GRANT ALL ON All ROUTINES IN SCHEMA public TO {username}; 
    '''
        
    with DbConnectionManager(get_admin_connection(event.db_name)) as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(filling_command)
                cursor.execute(user_creation_command)
                db_info.status = DatabaseStatus.UP.value
            except SQLError as error:
                db_info.status = DatabaseStatus.ERROR.value
                raise
                
            db_info.save()


def create_db(user_id: int, task_id: int, db_name: str) -> None:
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
            except SQLError as err:
                db_info.status = DatabaseStatus.ERROR.value
                db_info.save()
                raise
    
    return db_username, db_password


def delete_db(event: events.TaskDisposed, 
              message_queue: list) -> None:
    db_info = get_db_info(event.db_name)
    db_username = db_info.user.get_db_username()
    admin_db_name: str = SANDBOX_POSTGRES_DB
    
    with DbConnectionManager(get_admin_connection(admin_db_name)) as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(f'DROP DATABASE {event.db_name};')
                cursor.execute(f'DROP ROLE {db_username};')
                db_info.delete()
            except SQLError as err:       
                db_info.status = DatabaseStatus.ERROR.value
                db_info.save()
                raise


HANDLERS = {
    commands.CreateUserTask: create_user_task,
    commands.FinishUserTask: finish_user_task,
    commands.DeleteUserTaskDb: delete_user_task_db,
    commands.SendSqlCommand: send_sql_command,
    commands.CheckTask: check_task,
    events.DbCreated: [fill_task_db],
    events.TaskDisposed: [delete_db],
}
