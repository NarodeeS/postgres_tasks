from typing import TypedDict

import psycopg2

from .utils.get_database_connection import get_database_connection
from .utils.connection_manager import ConnectionManager


class QueryResult(TypedDict):
    status: str
    result: list | None
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
            except psycopg2.Error as exc:
                return QueryResult(status=cursor.statusmessage, 
                                   result=None, 
                                   error_message=exc.pgerror)
            
            return QueryResult(status=cursor.statusmessage, 
                               result=result, 
                               error_message=None)


def check_task_completion(db_name: str):
    pass
