import psycopg2

from .get_database_connection import get_admin_connection
from .database_status import DatabaseStatus
from .connection_manager import ConnectionManager
from core.models import DatabaseInfo


def fill_db(db_name: str, username: str, password: str):
    #  get from db
    filling_command = '''
        CREATE TABLE test_table(name TEXT, number INT);
        INSERT INTO test_table VALUES ('User', 1), ('Hello', 2);
    '''
    user_creation_command = f'''
        CREATE ROLE {username} WITH LOGIN PASSWORD '{password}';
        GRANT ALL ON SCHEMA public TO {username};
        GRANT ALL ON All TABLES IN SCHEMA public TO {username};
        GRANT ALL ON All SEQUENCES IN SCHEMA public TO {username};
        GRANT ALL ON All FUNCTIONS IN SCHEMA public TO {username};
        GRANT ALL ON All PROCEDURES IN SCHEMA public TO {username};
        GRANT ALL ON All ROUTINES IN SCHEMA public TO {username}; 
    '''
    
    db_info = DatabaseInfo.objects.get(db_name=db_name)
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
