from rest_framework import status
from rest_framework.exceptions import APIException


class BadRequestError(APIException):
    def __init__(self, message):
        self.detail = {'detail': message}
        self.status_code = status.HTTP_400_BAD_REQUEST 
