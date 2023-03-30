import psycopg2

from core.utils.get_database_connection import get_admin_connection
from .database_status import DatabaseStatus
from core.utils.connection_manager import ConnectionManager
from core.utils.load_script import load_script
from .utils.get_db_info import get_db_info


def fill_task_db(db_name: str, username: str, password: str):
    '''
    Filling db based on task. Can raise NoSuchDbError
    '''
    db_info = get_db_info(db_name)
        
    task = db_info.task
    filling_command = load_script(task.creation_script.path)
    
    user_creation_command = f'''
        CREATE ROLE {username} WITH LOGIN PASSWORD '{password}';
        GRANT ALL ON SCHEMA public TO {username};
        GRANT ALL ON All TABLES IN SCHEMA public TO {username};
        GRANT ALL ON All SEQUENCES IN SCHEMA public TO {username};
        GRANT ALL ON All FUNCTIONS IN SCHEMA public TO {username};
        GRANT ALL ON All PROCEDURES IN SCHEMA public TO {username};
        GRANT ALL ON All ROUTINES IN SCHEMA public TO {username}; 
    '''
        
    with ConnectionManager(get_admin_connection(db_name)) as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(filling_command)
                cursor.execute(user_creation_command)
                db_info.status = DatabaseStatus.UP.value
            except psycopg2.Error as error:
                print(error.pgerror)
                db_info.status = DatabaseStatus.ERROR.value
                
            db_info.save()
