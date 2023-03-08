import os

from psycopg2 import connect, extensions


def get_database_connection(db_name: str, username: str, password: str):
    connection = connect(host='sandbox_postgres',
                         port=5432,
                         user=username,
                         password=password,
                         database=db_name
    )
    connection.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    return connection


def get_admin_connection(db_name: str):
    return get_database_connection(db_name, 
                                   os.getenv('POSTGRES_USER'), # type: ignore
                                   os.getenv('POSTGRES_PASSWORD'))  # type: ignore
