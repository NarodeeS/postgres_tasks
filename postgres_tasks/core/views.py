from django.shortcuts import render
from django import views
from rest_framework import views
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework import status

from .tasks import create_db, delete_db


class HomeView(views.View):
    def get(self, request):
        return render(request, 'core/index.html')


class DbViewCreate(views.APIView):
    def post(self, request: HttpRequest) -> Response:
        create_db.delay()
        return Response({'detail': 'OK'}, status==status.HTTP_200_OK)


class DbViewDelete(views.APIView):
    def delete(self, request: HttpRequest, db_name: str) -> Response:
        delete_db.delay(db_name)
        return Response({'detail': 'OK'}, status=status.HTTP_200_OK)
