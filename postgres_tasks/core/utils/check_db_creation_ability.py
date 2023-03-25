from core.models import DatabaseInfo, UserTask
from .web_error_data import WebErrorData


def check_db_creation_ability(user_task_id: int) -> WebErrorData | None:
    if not user_task_id:  
        return WebErrorData(data={'detail': 'Need to specify user_task_id'}, 
                            status=400)
    
    if DatabaseInfo.objects.filter(user_task__id=user_task_id).exists():
        return WebErrorData(data={'detail': 'Db for this task already exists'}, 
                            status=400)

    return None
