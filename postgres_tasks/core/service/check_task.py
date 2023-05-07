import psycopg2

from core.utils.db_utils import get_admin_connection, DbConnectionManager
from core.utils.load_file import load_file
from .service_utils import get_db_info


def check_task(db_name: str) -> bool:
    '''
    Check task completion based on db name. Can raise NoSuchDbError
    '''
    db_info = get_db_info(db_name)
    
    check_script_path = db_info.task.check_script.path
    check_script = load_file(check_script_path)
    
    connection = get_admin_connection(db_name)
    
    with DbConnectionManager(connection):
        with connection.cursor() as cursor:
            try:
                cursor.execute(check_script)
                row = cursor.fetchone()
                if row:    
                    success, *_ = row
                    return bool(success)
            except psycopg2.Error as error:
                print(error.pgerror)
            
            return False
