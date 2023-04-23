from psycopg2 import connect, extensions

from config import POSTGRES_USER, POSTGRES_PASSWORD


def get_database_connection(db_name: str, username: str, password: str):
    connection = connect(host='sandbox-postgres',
                         port=5432,
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
