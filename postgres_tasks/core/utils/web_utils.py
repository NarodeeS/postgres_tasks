from rest_framework import status
from rest_framework.response import Response


def not_found(message: str):
    return Response(data={'detail': message},
                    status=status.HTTP_404_NOT_FOUND)


def bad_request(message: str):
    return Response(data={'detail': message}, 
                    status=status.HTTP_400_BAD_REQUEST)


def ok(data: dict | None = None):
    if data is None:
        data = {'detail': 'OK'}
    return Response(data=data, 
                    status=status.HTTP_200_OK)
