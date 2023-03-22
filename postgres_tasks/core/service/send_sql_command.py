from typing import TypedDict

import psycopg2

from core.utils.get_database_connection import get_database_connection
from core.utils.connection_manager import ConnectionManager
from core.models import DatabaseInfo


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
    db_info = DatabaseInfo.objects.filter(db_name=db_name).first()
    task = db_info.get_task()  # type: ignore
    
    username = 'test_user'
    password = 'test_password'
    
    # can raise operational error, if db or user don't exists
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
