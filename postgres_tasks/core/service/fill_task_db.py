import psycopg2

from core.utils.get_database_connection import get_admin_connection
from .database_status import DatabaseStatus
from core.utils.connection_manager import ConnectionManager
from core.models import DatabaseInfo
from core.utils.load_script import load_script


def fill_task_db(db_name: str, username: str, password: str):
    db_info: DatabaseInfo = (DatabaseInfo.objects
                                         .filter(db_name=db_name)
                                         .first()) # type: ignore
        
    task = db_info.get_task()
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
            except psycopg2.Error as err:
                print(err.pgerror)
                db_info.status = DatabaseStatus.ERROR.value
                
            db_info.save()
