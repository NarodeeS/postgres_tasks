from core.serializers import TaskGetSerializer
from core.models import CompletedTask, Task, User
from core.utils.raise_if_not_exsts import raise_if_not_exists
from core.utils.database_exists import database_exists
from core.tasks import create_db_task
from core.service.errors import TaskAlreadyStartedError, NoSuchTaskError


def get_user_task_data(task_id: int) -> dict:
    task_model = Task.objects.filter(id=task_id).first()
    raise_if_not_exists(task_model, 'No such task')
    
    associated_user_task = (CompletedTask.objects.filter(task__id=task_id)
                                                 .first())
    
    task = TaskGetSerializer(instance=task_model).data
    task['completed'] = True if associated_user_task else False
    return task
 

def get_user_tasks_data(user: User):
    all_tasks = [TaskGetSerializer(instance=task).data 
                    for task in Task.objects.all()]
    user_tasks = {user_task.task.id: user_task
                    for user_task in (CompletedTask.objects
                                                   .filter(user=user))}
    for task in all_tasks:
        associated_user_task = user_tasks.get(task['id'])
        task['completed'] = True if associated_user_task else False
        
    return all_tasks


def create_user_task(task_id: int, user: User) -> str:
    task = Task.objects.filter(id=task_id).first()
    if not task:
        raise NoSuchTaskError(task)
    
    db_name = f"{'_'.join(task.title.split(' ')).lower()}_{user.id}"
    if not (db_info := database_exists(user.id)):
        create_db_task.delay(user.id, task.id, db_name)
    else:
        if db_info.task.id != task_id:
            raise TaskAlreadyStartedError(db_info.task.id)
    return db_name
