from django.shortcuts import render
from django import views
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from .tasks import create_db, delete_db
from .models import DatabaseInfo
from .serializers import DatabaseInfoSerializer
from .service import send_sql_command, check_task_completion

class DbCreateView(views.APIView):
    def post(self, request, *args, **kwargs) -> Response:
        task_name = request.data.get('task_name')
        db_name = 'test_db'  # generate based on username and task name
        
        if not task_name:  
            return Response(data={'detail': 'Need to specify task_name'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        # also check task existance
        
        if DatabaseInfo.objects.filter(db_name=db_name).exists():
            return Response(data={'detail': 'Such db already exists'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        create_db.delay('test_db')
        return Response({'detail': 'OK'}, status=status.HTTP_200_OK)


class DbGetDeleteView(generics.RetrieveDestroyAPIView):
    queryset = DatabaseInfo.objects.all()
    serializer_class = DatabaseInfoSerializer
    lookup_field = 'db_name'
    
    def delete(self, request, *args, **kwargs):
        db_name = kwargs.get('db_name')
        if db_name is None:
            return Response(data={'detail': 'Use db_name as path parameter'}, 
                            status=status.HTTP_404_NOT_FOUND)
    
        if not DatabaseInfo.objects.filter(db_name=db_name).exists():
            return Response({'detail': 'No such db'}, 
                            status=status.HTTP_404_NOT_FOUND)

        delete_db.delay(db_name)
        return Response({'detail': 'OK'}, status=status.HTTP_200_OK)


class DbCommandView(views.APIView):
    def post(self, request, *args, **kwargs):
        try:
            db_name = kwargs['db_name']
            sql_query = request.data['command']
            
        except KeyError as err:
            return Response(data={'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)
        
        if not DatabaseInfo.objects.filter(db_name=db_name).exists():
            return Response(data={'detail': "db don't exists"},
                            status=status.HTTP_404_NOT_FOUND)
            
        result = send_sql_command(db_name, sql_query)

        if (err_msg := result['error_message']) is not None:
            return Response(data={'error': err_msg}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'status': result['status'], 
                              'result': result['result'],
                              'columns': result['columns']}, 
                        status=status.HTTP_200_OK)


class DbCheckView(views.APIView):
    def post(self, request, *args, **kwargs):
        try:
            db_name = kwargs['db_name']
        except KeyError:
            return Response(data={'detail': 'Use db_name as path parameter'}, 
                            status=status.HTTP_404_NOT_FOUND)
        
        if not DatabaseInfo.objects.filter(db_name=db_name).exists():
            return Response(data={'detail': "db don't exists"},
                            status=status.HTTP_404_NOT_FOUND)
            
        success = check_task_completion(db_name)
        
        if success:
            response_message = 'Task completed sucessfully'
            response_status = status.HTTP_200_OK
            
            delete_db.delay(db_name)
        else:
            response_message = 'Check error'
            response_status = status.HTTP_400_BAD_REQUEST
        
        return Response(data={'detail': response_message}, 
                        status=response_status)
