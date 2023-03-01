from rest_framework import views
from rest_framework.request import Request
from rest_framework.response import Response


class HomeView(views.APIView):
    def get(self, request: Request) -> Response:
        return Response(data={'message': 'Hello, DRF!'})
