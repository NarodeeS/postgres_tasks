from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from core.models import User
from core.utils.web_utils import bad_request, ok


class EmaillApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            email = request.data["email"]
        except KeyError:
            return bad_request('Need to specify email')
        try:
            key = request.data["key"]
        except KeyError:
            return bad_request('Need to specify key')
        
        cashed_key = cache.get(email)
        print(cashed_key)

        if cashed_key != int(key):
            return bad_request('Wrong key')
        
        user = User.objects.filter(email=email).first()
        print(user)
        if not user:
            return bad_request('No such user')
        
        user.email_confirmed = True
        user.save()
        cache.delete(email)

        return ok()
