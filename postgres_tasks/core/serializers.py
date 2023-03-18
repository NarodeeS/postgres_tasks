from rest_framework import serializers

from .models import DatabaseInfo, Task, ActiveTask


class DatabaseInfoSerializer(serializers.ModelSerializer):
    task_name = serializers.CharField(max_length=255, write_only=True)
    
    class Meta:
        model = DatabaseInfo
        fields = ['id', 'db_name', 'status', 'task_name']
        read_only_fields = ['id', 'db_name', 'status']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'difficulty']


class ActiveTaskSerializer(serializers.ModelSerializer):
    task = TaskSerializer()
    
    class Meta:
        model = ActiveTask
        fields = '__all__'
        depth = 1

