from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer

from core.celery_tasks import send_verification_email 
from .models import DatabaseInfo, Task, User
from postgres_tasks.settings import VERIFICATE_EMAIL

class DatabaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseInfo
        fields = ('id', 'db_name', 'status', 'moves_left')


class TaskGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'difficulty')


class UserRegistrationSerializer(BaseUserRegistrationSerializer):

    def validate(self, data):
        super().validate(data)
        email = data.get("email")
        if VERIFICATE_EMAIL == True:
            send_verification_email.delay(email)
        else:
            data['email_confirmed'] = True
        return data

    class Meta(BaseUserRegistrationSerializer.Meta):
        model = User
        fields = ('first_name', 'last_name', 'student_group', 'email', 'password')
