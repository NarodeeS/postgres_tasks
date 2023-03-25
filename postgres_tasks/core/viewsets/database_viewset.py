from rest_framework import (viewsets, status, 
                            permissions)
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import DatabaseInfo
from core.serializers import DatabaseInfoSerializer
from core.permissions import IsOwner
from core.celery_tasks import delete_db, create_db
from core.service.send_sql_command import send_sql_command
from core.service.check_task import check_task
from core.service.errors import NoSuchDbError, NoSuchUserTask
from core.service.utils.finish_task import finish_task
from core.service.utils.get_user_task import get_user_task
from core.utils.check_db_creation_ability import check_db_creation_ability


class DatabaseViewSet(viewsets.ModelViewSet):
    queryset = DatabaseInfo.objects.all()
    serializer_class = DatabaseInfoSerializer
    lookup_field = 'db_name'
    permission_classes = [IsOwner & permissions.IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(user_task__user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        user_task_id = request.data.get('user_task')
        user = request.user
        
        if (err_info := check_db_creation_ability(user_task_id, 
                                                  user.id)) is None:
            try:
                user_task = get_user_task(user_task_id)
                db_name = f"{user.username}_{'_'.join(user_task.task.title.split(' ')).lower()}"
            except NoSuchUserTask as error:
                return Response(data={'error': str(error)}, 
                                status=status.HTTP_400_BAD_REQUEST)      
                  
            create_db.delay(user_task_id, db_name)
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
            
        try:
            result = send_sql_command(db_name, sql_query)
        except NoSuchDbError as error:
            return Response(data={'error': str(error)}, 
                            status=status.HTTP_400_BAD_REQUEST)
            
        return Response(data=result, 
                        status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def check(self, request, *args, **kwargs):
        try:
            db_name = kwargs['db_name']
        except KeyError:
            return Response(data={'detail': 'Use db_name as path parameter'}, 
                            status=status.HTTP_404_NOT_FOUND)
        
        try:
            success = check_task(db_name)
        except NoSuchDbError as error:
            return Response(data={'error': str(error)}, 
                            status=status.HTTP_400_BAD_REQUEST)
            
        response_status = status.HTTP_200_OK
        if success:
            response_message = 'Task completed sucessfully'
            finish_task(db_name)
        else:
            response_message = 'Check error'
        
        return Response(data={'detail': response_message}, 
                        status=response_status)
