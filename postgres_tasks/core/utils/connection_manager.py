class ConnectionManager:
    def __init__(self, psycopg_connection) -> None:
        self.psycopg_connection = psycopg_connection
    
    def __enter__(self):
        return self.psycopg_connection
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.psycopg_connection.commit()
        self.psycopg_connection.close()
