import psycopg2

from core.models import DatabaseInfo
from core.utils.get_database_connection import get_admin_connection
from core.utils.connection_manager import ConnectionManager
from core.utils.load_script import load_script


def check_task(db_name: str) -> bool:
    db_info = DatabaseInfo.objects.filter(db_name=db_name).first()
    if db_info:
        check_script_path = db_info.user_task.active_task.task.check_script.path
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
                except psycopg2.Error as err:
                    print(err.pgerror)
                
                return False
    return False
