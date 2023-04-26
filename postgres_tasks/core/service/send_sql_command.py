from typing import TypedDict

import psycopg2

from core.utils.get_database_connection import get_database_connection
from core.utils.connection_manager import ConnectionManager
from core.service.errors import OutOfMovesError
from .utils.get_db_info import get_db_info


class QueryResult(TypedDict):
    status: str
    result: list | None
    columns: list[str] | None
    error_message: str | None
    moves_left: int 


def send_sql_command(db_name: str, command: str) -> QueryResult:
    '''
    Allow to send SQL-commands to db. Can raise NoSuchDbError
    '''
    db_info = get_db_info(db_name)
        
    db_username =  db_info.user.get_db_username()
    db_password = db_info.db_password
    
    connection = get_database_connection(db_name, db_username, db_password)
    
    with ConnectionManager(connection):
        with connection.cursor() as cursor:
            try:
                if db_info.moves_performed >= db_info.task.moves_count:
                    raise OutOfMovesError()
                db_info.increment_moves()
                cursor.execute(command)
                result = cursor.fetchall()
                column_names = [descr_row[0] for descr_row in cursor.description]
            except psycopg2.Error as error:
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
