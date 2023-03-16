from rest_framework import serializers

from .models import DatabaseInfo, Task, ActiveTask


class DatabaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseInfo
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'difficulty']


class ActiveTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveTask
        fields = '__all__'
