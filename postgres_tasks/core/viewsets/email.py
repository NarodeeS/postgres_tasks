from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from core.models import User
from django.core.cache import cache


class EamilApiView(APIView):

    def post(self, request):
        try:
            email = request.data["email"]
        except KeyError:
            return Response(data={'error': 'Need to specify email'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            key = request.data["key"]
        except KeyError:
            return Response(data={'error': 'Need to specify key'},
                            status=status.HTTP_400_BAD_REQUEST) 
        
        cashed_key = cache.get(email)
        print(cashed_key)

        if cashed_key != int(key):
            return Response(data={'error': 'Wrong key'},
                            status=status.HTTP_400_BAD_REQUEST) 
        
        user = User.objects.filter(email=email).first()
        print(user)
        if not user:
            return Response(data={'error': 'No such user'},
                            status=status.HTTP_400_BAD_REQUEST)
        user.email_confirmed = True
        user.save()
        cache.delete(email)

        return Response(data={'detail': 'OK'}, 
                            status=status.HTTP_200_OK)

