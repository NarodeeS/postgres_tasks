from django.shortcuts import render
from django import views
from rest_framework import views
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from .tasks import create_db, delete_db
from .models import DatabaseInfo
from .serializers import DatabaseInfoSerializer
from .service import send_sql_command


class HomeView(views.View):
    def get(self, request):
        return render(request, 'core/index.html')


class DbViewCreate(views.APIView):
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


class DbViewGetDelete(generics.RetrieveDestroyAPIView):
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

        delete_db.delay(kwargs['db_name'])
        return Response({'detail': 'OK'}, status=status.HTTP_200_OK)


class DbViewCommand(views.APIView):
    def post(self, request, *args, **kwargs):
        try:
            db_name = kwargs['db_name']
            sql_query = request.data['command']
            result = send_sql_command(db_name, sql_query)
            if (err_msg := result['error_message']) is not None:
                return Response(data={'error': err_msg}, status=status.HTTP_400_BAD_REQUEST)
            return Response(data={'status': result['status'], 
                                  'result': result['result']}, 
                            status=status.HTTP_200_OK)
            
        except KeyError as err:
            return Response(data={'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)
