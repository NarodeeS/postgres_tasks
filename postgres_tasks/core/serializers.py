from rest_framework import serializers
from djoser.serializers import UserCreateSerializer

from .models import DatabaseInfo, Task


class DatabaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseInfo
        exclude = ['db_password', 'task', 'user']
        read_only_fields = ['id', 'db_name', 'status']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'difficulty']


class UserRegistrationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ('name', 'surname', 'student_group', 'email', 'password')
