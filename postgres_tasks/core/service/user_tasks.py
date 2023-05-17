from core.serializers import TaskGetSerializer
from core.models import CompletedTask, Task, User
from domain.errors import NoSuchTaskError


def get_user_task_data(task_id: int) -> dict:
    task = Task.objects.filter(id=task_id).first()
    if not task:
        raise NoSuchTaskError(task)
    
    associated_user_task = (CompletedTask.objects.filter(task__id=task_id)
                                                 .first())
    
    task = TaskGetSerializer(instance=task).data
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
