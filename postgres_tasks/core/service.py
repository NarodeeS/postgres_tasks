from typing import TypedDict

import psycopg2
from psycopg2 import errors

from .utils.get_database_connection import get_database_connection, get_admin_connection
from .utils.connection_manager import ConnectionManager


class QueryResult(TypedDict):
    status: str
    result: list | None
    columns: list[str] | None
    error_message: str | None


def send_sql_command(db_name: str, command: str) -> QueryResult:
    '''
    return command status and exception message
    '''
    #  get from db
    username = 'test_user'
    password = 'test_password'
    connection = get_database_connection(db_name, username, password)
    with ConnectionManager(connection):
        with connection.cursor() as cursor:
            try:
                cursor.execute(command)
                result = cursor.fetchall()
                column_names = [descr_row[0] for descr_row in cursor.description]
            except psycopg2.Error as exc:
                return QueryResult(status=cursor.statusmessage,
                                   result=None,
                                   columns=None,
                                   error_message=exc.pgerror)
            
            return QueryResult(status=cursor.statusmessage, 
                               result=result, 
                               columns=column_names,
                               error_message=None)
    

def check_task_completion(db_name: str) -> bool:
    with ConnectionManager(get_admin_connection(db_name)) as connection:
        with connection.cursor() as cursor:
            try:
                # check logic
                check_script = '''
                    SELECT * FROM users;
                '''
                columns = ['name', 'surname', 'age']
                cursor.execute(check_script)
                rows = cursor.fetchall()
                columns_names = [descr_row[0] for descr_row in cursor.description]
                return (len(rows) == 2 and columns_names == columns)
            
            except errors.Error as err:
                print({err.pgerror})
            
            return False
