class NoSuchDbError(Exception):
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
    
    def __str__(self) -> str:
        return f"Can't find '{self.db_name}' db"


class NoSuchTaskError(Exception):
    def __init__(self, task) -> None:
        self.task = task


class NoSuchUserTaskError(Exception):
    def __init__(self, user_task_id: int) -> None:
        self.user_task_id = user_task_id

    def __str__(self) -> str:
        return f"Can't find user task with id: {self.user_task_id}"


class OutOfMovesError(Exception):
    def __str__(self) -> str:
        return "You're out of moves!"


class TaskAlreadyStartedError(Exception):
    def __init__(self, started_task_id: int) -> None:
        self.started_task_id = started_task_id
