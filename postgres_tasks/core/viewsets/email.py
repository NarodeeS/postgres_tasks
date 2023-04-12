from rest_framework.views import APIView
from rest_framework.response import Response
from core.celery_tasks import send_verification_email 
from django.core.cache import cache


class EamilApiView(APIView):

    def get(self, request):
        email = "angron2002@mail.ru"
        print(cache.get(email))
        send_verification_email.delay(email)
        return Response({'message': ' was send'})