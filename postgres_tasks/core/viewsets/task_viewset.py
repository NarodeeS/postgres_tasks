from rest_framework import viewsets, status
from rest_framework.response import Response

from core.utils.common_responses import not_found
from core.service.user_tasks import (get_user_task_data, 
                                     get_user_tasks_data, 
                                     create_user_task)
from core.service.errors import TaskAlreadyStartedError, NoSuchTaskError


class TaskViewSet(viewsets.ViewSet):
    def retrieve(self, request, *args, **kwargs):        
        try:
            task_id = kwargs['task_id']
            task_data = get_user_task_data(task_id)
        except KeyError:
            return Response(data={'error': 'Need to specify task id'})
        except NoSuchTaskError as e:
            return not_found('No such task')
            
        return Response(data={'task': task_data},
                        status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        all_tasks_data = get_user_tasks_data(request.user)
        return Response(data=all_tasks_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        try:
            task_id = request.data['task_id']
        except KeyError:
            return Response(data={'error': 'Need to specify task_id'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        try:
            db_name = create_user_task(task_id, request.user)
        except NoSuchTaskError as e:
            return not_found('No such task')
        except TaskAlreadyStartedError as e:
            return Response(data={'detail': 'Another task already started', 
                                  'task_id': e.started_task_id}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data={'detail': 'OK', 'db_name': db_name},
                        status=status.HTTP_200_OK)
