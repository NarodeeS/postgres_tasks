from rest_framework import serializers

from .models import DatabaseInfo, Task, UserTask


class DatabaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseInfo
        exclude = ['db_password']
        read_only_fields = ['id', 'db_name', 'status']


class TaskGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'difficulty']
        

class TaskCreateSerializer(serializers.ModelSerializer):
    creation_script = serializers.FileField()
    check_script = serializers.FileField()
    db_structure = serializers.ImageField()
    
    class Meta:
        model = Task
        fields = '__all__'


class UserTaskSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = UserTask
        fields = '__all__'
        read_only_fields = ['id', 'completed']
