from rest_framework import (viewsets, mixins, 
                            status, permissions)
from rest_framework.decorators import action
from rest_framework.response import Response

from core.serializers import DatabaseInfoSerializer
from core.models import DatabaseInfo
from core.permissions import IsOwner
from core.tasks import delete_db
from core.service.send_sql_command import send_sql_command
from core.service.check_task import check_task
from core.service.errors import NoSuchDbError, OutOfMovesError
from core.service.utils.finish_task import finish_task
from core.utils.raise_if_not_exsts import raise_if_not_exists


class DatabaseViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin, 
                      viewsets.GenericViewSet):
    queryset = DatabaseInfo.objects.all()
    serializer_class = DatabaseInfoSerializer
    lookup_field = 'db_name'
    permission_classes = [IsOwner & permissions.IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        db_name = kwargs.get('db_name')
        raise_if_not_exists(db_name, 'Use db_name as path parameter')
        raise_if_not_exists((DatabaseInfo.objects
                                         .filter(db_name=db_name)
                                         .first()), 
                            'No such db')

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
        except (NoSuchDbError, OutOfMovesError) as error:
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
