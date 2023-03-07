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


class HomeView(views.View):
    def get(self, request):
        return render(request, 'core/index.html')


class DbViewCreate(views.APIView):
    def post(self, request: HttpRequest) -> Response:
        create_db.delay()
        return Response({'detail': 'OK'}, status=status.HTTP_200_OK)


class DbViewGetDelete(generics.RetrieveDestroyAPIView):
    queryset = DatabaseInfo.objects.all()
    serializer_class = DatabaseInfoSerializer
    lookup_field = 'db_name'
    
    def delete(self, request, *args, **kwargs):
        db_name = kwargs.get('db_name')
        if db_name is None:
            return Response(data={'error': "Use db_name as path parameter"})
        delete_db.delay(kwargs['db_name'])
        return Response({'detail': 'OK'}, status=status.HTTP_200_OK)
