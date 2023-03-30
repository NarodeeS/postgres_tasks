from core.models import CompletedTask
from .get_db_info import get_db_info
from core.celery_tasks import delete_db


def finish_task(db_name: str):
    '''
    Create 'CompletedTask' and delete db for this task
    '''
    db_info = get_db_info(db_name)
    potential_completed_task = (CompletedTask.objects
                                             .filter(task__id=db_info.task.id, 
                                                     user__id=db_info.user.id))
    if not potential_completed_task:
        CompletedTask.objects.create(task=db_info.task, 
                                     user=db_info.user)
    delete_db.delay(db_name)
