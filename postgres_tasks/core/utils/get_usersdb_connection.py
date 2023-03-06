import os
from psycopg2 import connect, extensions


def get_usersdb_connection():
    connection = connect(host='sandbox_postgres',
                         port=5432,
                         user=os.getenv("POSTGRES_USER"),
                         password=os.getenv("POSTGRES_PASSWORD"),
                         database=os.getenv("POSTGRES_DB")
    )
    connection.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    return connection
