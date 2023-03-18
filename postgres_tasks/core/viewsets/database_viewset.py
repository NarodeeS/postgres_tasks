from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import DatabaseInfo
from core.serializers import DatabaseInfoSerializer
from core.celery_tasks import delete_db, create_db
from core.service.send_sql_command import send_sql_command
from core.service.check_task import check_task
from core.utils.check_db_creation_ability import check_db_creation_ability


class DatabaseViewSet(viewsets.ModelViewSet):
    queryset = DatabaseInfo.objects.all()
    serializer_class = DatabaseInfoSerializer
    lookup_field = 'db_name'
    
    def create(self, request, *args, **kwargs):
        task_name = request.data.get('task_name')
        db_name = task_name  # generate based on username and task name
        
        if (err_info := check_db_creation_ability(db_name, task_name)) is None:
            create_db.delay(db_name)
            return Response(data={'detail': 'OK', 'db_name': db_name}, 
                            status=status.HTTP_200_OK)
        
        return Response(**err_info)
    
    def destroy(self, request, *args, **kwargs):
        db_name = kwargs.get('db_name')
        if db_name is None:
            return Response(data={'detail': 'Use db_name as path parameter'}, 
                            status=status.HTTP_404_NOT_FOUND)
    
        if not DatabaseInfo.objects.filter(db_name=db_name).exists():
            return Response({'detail': 'No such db'}, 
                            status=status.HTTP_404_NOT_FOUND)

        delete_db.delay(db_name)
        return Response({'detail': 'OK'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def command(self, request, *args, **kwargs):
        try:
            db_name = kwargs['db_name']
            sql_query = request.data['command']
            
        except KeyError as err:
            return Response(data={'error': str(err)}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        if not DatabaseInfo.objects.filter(db_name=db_name).exists():
            return Response(data={'detail': "db don't exists"},
                            status=status.HTTP_404_NOT_FOUND)
            
        result = send_sql_command(db_name, sql_query)

        if (err_msg := result['error_message']) is not None:
            return Response(data={'error': err_msg}, 
                            status=status.HTTP_400_BAD_REQUEST)
            
        return Response(data={'status': result['status'], 
                              'result': result['result'],
                              'columns': result['columns']}, 
                        status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def check(self, request, *args, **kwargs):
        try:
            db_name = kwargs['db_name']
        except KeyError:
            return Response(data={'detail': 'Use db_name as path parameter'}, 
                            status=status.HTTP_404_NOT_FOUND)
        
        if not DatabaseInfo.objects.filter(db_name=db_name).exists():
            return Response(data={'detail': "db don't exists"},
                            status=status.HTTP_404_NOT_FOUND)
            
        success = check_task(db_name)
        
        if success:
            response_message = 'Task completed sucessfully'
            response_status = status.HTTP_200_OK
            
            delete_db.delay(db_name)
        else:
            response_message = 'Check error'
            response_status = status.HTTP_400_BAD_REQUEST
        
        return Response(data={'detail': response_message}, 
                        status=response_status)
