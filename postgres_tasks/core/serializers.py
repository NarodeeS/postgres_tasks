from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer

from core.celery_tasks import send_verification_email 
from .models import DatabaseInfo, Task, User


class DatabaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseInfo
        exclude = ['db_password', 'task', 'user']
        read_only_fields = ['id', 'db_name', 'status']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'difficulty']


class UserRegistrationSerializer(BaseUserRegistrationSerializer):

    def validate(self, attrs):
        email = attrs.get("email")
        send_verification_email.delay(email)
        return super().validate(attrs)

    class Meta(BaseUserRegistrationSerializer.Meta):
        model = User
        fields = ('first_name', 'last_name', 'student_group', 'email', 'password')
