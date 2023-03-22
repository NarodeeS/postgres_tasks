from core.models import DatabaseInfo, UserTask
from .web_error_data import WebErrorData


def check_db_creation_ability(db_name: str, task_name: str) -> WebErrorData | None:
    if not task_name:  
        return WebErrorData(data={'detail': 'Need to specify task_name'}, 
                            status=400)
            
    
    # also check for current user
    if not UserTask.objects.filter(active_task__task__title=task_name).exists():
        return  WebErrorData(data={'detail': f'Can\'t find task with name {task_name} for such user'}, 
                             status=400)
        
    
    # check if database for such task exists
    if DatabaseInfo.objects.filter(db_name=db_name).exists():
        return WebErrorData(data={'detail': 'Such db already exists'}, 
                            status=400)

    return None
