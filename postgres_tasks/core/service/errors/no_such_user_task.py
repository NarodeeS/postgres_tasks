class NoSuchUserTask(Exception):
    def __init__(self, user_task_id: int) -> None:
        self.user_task_id = user_task_id

    def __str__(self) -> str:
        return f"Can't find user task with id: {self.user_task_id}"
