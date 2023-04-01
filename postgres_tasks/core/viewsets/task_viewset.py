from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from core.models import Task, CompletedTask
from core.serializers import TaskSerializer
from core.utils.raise_if_not_exsts import raise_if_not_exists
from core.utils.database_exists import database_exists
from core.celery_tasks import create_db


class TaskViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):        
        try:
            task_id = kwargs['task_id']
        except KeyError:
            return Response(data={'error': 'Need to specify task id'})

        task_model = Task.objects.filter(id=task_id).first()
        raise_if_not_exists(task_model, 'No such task')
        
        associated_user_task = CompletedTask.objects.filter(task__id=task_id).first()
        
        task = TaskSerializer(instance=task_model).data
        task['completed'] = True if associated_user_task else False

        return Response(data={'task': task}, 
                        status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        all_tasks = [TaskSerializer(instance=task).data 
                     for task in Task.objects.all()]
        user_tasks = {user_task.task.id: user_task
                      for user_task in (CompletedTask.objects
                                                .filter(user=request.user))}
        for task in all_tasks:
            associated_user_task = user_tasks.get(task['id'])
            task['completed'] = True if associated_user_task else False
            
        return Response(data=all_tasks, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        try:
            task_id = request.data['task_id']
        except KeyError:
            return Response(data={'error': 'Need to specify task_id'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        task: Task = Task.objects.filter(id=task_id).first() # type: ignore
        raise_if_not_exists(task, 'No such task')

        db_name = f"{'_'.join(task.title.split(' ')).lower()}_{user.id}"
        if not database_exists(user.id):
            create_db.delay(request.user.id, task.id, db_name)
            
        return Response(data={'detail': 'OK', 'db_name': db_name}, 
                        status=status.HTTP_200_OK)
