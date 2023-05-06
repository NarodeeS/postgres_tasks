from rest_framework import status
from rest_framework.response import Response


def not_found(message: str):
    return Response(data={'detail': message},
                    status=status.HTTP_404_NOT_FOUND)
