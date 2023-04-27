from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.serializers import DatabaseInfoSerializer
from core.models import DatabaseInfo
from core.permissions import IsOwner, IsEmailVerifiedAndAuthenticated
from core.service.delete_db import delete_db
from core.service.send_sql_command import send_sql_command
from core.service.check_task import check_task
from core.service.errors import NoSuchDbError, OutOfMovesError
from core.service.finish_task import finish_task


class DatabaseViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin, 
                      viewsets.GenericViewSet):
    queryset = DatabaseInfo.objects.all()
    serializer_class = DatabaseInfoSerializer
    lookup_field = 'db_name'
    permission_classes = [IsOwner & IsEmailVerifiedAndAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        try:
            db_name = kwargs['db_name']
            delete_db(db_name)
        except KeyError:
            return Response(data={'detail': 'Use db_name as path parameter'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        except NoSuchDbError as e:
            return Response(data={'detail': str(e)}, 
                            status=status.HTTP_400_BAD_REQUEST)

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
