from core.models import UserTask
from ..errors.no_such_user_task import NoSuchUserTask


def get_user_task(user_task_id: int):
    potential_user_task = (UserTask.objects
                                   .filter(id=user_task_id)
                                   .first())
    if not potential_user_task:
        raise NoSuchUserTask(user_task_id)
    return potential_user_task
