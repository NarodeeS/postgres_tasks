from core.models import DatabaseInfo, ActiveTask
from .web_error_data import WebErrorData


def check_db_creation_ability(db_name: str, task_name: str) -> WebErrorData | None:
    if not task_name:  
        return WebErrorData(data={'detail': 'Need to specify task_name'}, 
                            status=400)
            
    
    if not ActiveTask.objects.filter(task__title=task_name).exists():
        return  WebErrorData(data={'detail': f'Can\'t find tasj with name {task_name}'}, 
                             status=400)
        
    
    if DatabaseInfo.objects.filter(db_name=db_name).exists():
        return WebErrorData(data={'detail': 'Such db already exists'}, 
                            status=400)

    return None
