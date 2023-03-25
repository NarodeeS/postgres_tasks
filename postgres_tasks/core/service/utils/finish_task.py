from .get_db_info import get_db_info
from core.celery_tasks import delete_db


def finish_task(db_name: str):
    '''
    Set UserTask as completed and delete db for this task
    '''
    db_info = get_db_info(db_name)
    
    db_info.user_task.completed = True
    db_info.user_task.save()
    delete_db.delay(db_name)
