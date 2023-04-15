class NoSuchDbError(Exception):
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
    
    def __str__(self) -> str:
        return f"Can't find '{self.db_name}' db"
