import psycopg2

from core.utils.get_database_connection import get_admin_connection
from core.utils.connection_manager import ConnectionManager
from core.utils.load_script import load_script
from .utils.get_db_info import get_db_info


def check_task(db_name: str) -> bool:
    '''
    Check task completion based on db name. Can raise NoSuchDbError
    '''
    db_info = get_db_info(db_name)
    
    check_script_path = db_info.task.check_script.path
    check_script = load_script(check_script_path)
    
    connection = get_admin_connection(db_name)
    
    with ConnectionManager(connection):
        with connection.cursor() as cursor:
            try:
                cursor.execute(check_script)
                row = cursor.fetchone()
                if row:    
                    success, *_ = row
                    if success:
                        return True
                    else:
                        return False
            except psycopg2.Error as error:
                print(error.pgerror)
            
            return False
