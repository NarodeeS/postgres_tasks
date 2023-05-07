from rest_framework import viewsets

from core.utils.web_utils import not_found, bad_request, ok
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
            return bad_request('Need to specify task id')
        except NoSuchTaskError:
            return not_found('No such task')
        
        return ok({'task': task_data})

    def list(self, request, *args, **kwargs):
        all_tasks_data = get_user_tasks_data(request.user)
        return ok(all_tasks_data)

    def create(self, request, *args, **kwargs):
        try:
            task_id = request.data['task_id']
        except KeyError:
            return bad_request('Need to specify task_id')
        
        try:
            db_name = create_user_task(task_id, request.user)
        except NoSuchTaskError as e:
            return not_found('No such task')
        except TaskAlreadyStartedError as e:
            return bad_request({'detail': 'Another task already started', 
                                'task_id': e.started_task_id})
        
        return ok({'detail': 'OK', 'db_name': db_name})
