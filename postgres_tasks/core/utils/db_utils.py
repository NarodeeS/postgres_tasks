from psycopg2 import connect, extensions

from config import (POSTGRES_USER, 
                    POSTGRES_PASSWORD, 
                    SANDBOX_POSTGRES_HOST, 
                    SANDBOX_POSTGRES_PORT)
from core.models import DatabaseInfo
from domain.errors import NoSuchDbError


class DbConnectionManager:
    def __init__(self, psycopg_connection) -> None:
        self.psycopg_connection = psycopg_connection
    
    def __enter__(self):
        return self.psycopg_connection
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.psycopg_connection.commit()
        self.psycopg_connection.close()


def database_exists(user_id: int) -> DatabaseInfo | None:
    return DatabaseInfo.objects.filter(user__id=user_id).first()


def get_db_info(db_name: str) -> DatabaseInfo:
    potential_db_info = (DatabaseInfo.objects
                                     .filter(db_name=db_name)
                                     .first())
    if not potential_db_info:
        raise NoSuchDbError(db_name)
    return potential_db_info


def get_database_connection(db_name: str, username: str, password: str):
    connection = connect(host=SANDBOX_POSTGRES_HOST,
                         port=SANDBOX_POSTGRES_PORT,
                         user=username,
                         password=password,
                         database=db_name
    )
    connection.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    return connection


def get_admin_connection(db_name: str):
    return get_database_connection(db_name, 
                                   POSTGRES_USER, # type: ignore
                                   POSTGRES_PASSWORD)  # type: ignore
