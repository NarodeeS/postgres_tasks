from rest_framework import viewsets, mixins, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from core.serializers import DatabaseInfoSerializer
from core.models import DatabaseInfo
from core.permissions import IsOwner
from core.bootstrap import bootstrap
from domain.errors import NoSuchDbError, OutOfMovesError
from domain import commands
from core.utils.web_utils import bad_request, not_found, ok


bus = bootstrap()


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
        try:
            db_name = kwargs['db_name']
            bus.handle(commands.DeleteUserTaskDb(db_name))
        except KeyError:
            return bad_request('Use db_name as path parameter')
        except NoSuchDbError as e:
            return bad_request(str(e))
        
        return ok()
    
    @action(detail=True, methods=['post'])
    def command(self, request, *args, **kwargs):
        try:
            db_name = kwargs['db_name']
            sql_query = request.data['command']
        except KeyError:
            return bad_request("Use 'db_name' in query " 
                               "parameters and 'command' in body")
            
        try:
            result = bus.handle(commands.SendSqlCommand(db_name, sql_query))
        except (NoSuchDbError, OutOfMovesError) as error:
            return bad_request(str(error))
        
        return ok(result)
    
    @action(detail=True, methods=['post'])
    def check(self, request, *args, **kwargs):
        try:
            db_name = kwargs['db_name']
        except KeyError:
            return not_found('Use db_name as path parameter')
        
        try:
            success = bus.handle(commands.CheckTask(db_name))
        except NoSuchDbError as error:
            return bad_request(str(error))
            
        response_status = status.HTTP_200_OK
        if success:
            response_message = 'Task completed sucessfully'
            bus.handle(commands.FinishUserTask(db_name))
        else:
            response_message = 'Check error'
        
        return Response(data={'detail': response_message}, 
                        status=response_status)
