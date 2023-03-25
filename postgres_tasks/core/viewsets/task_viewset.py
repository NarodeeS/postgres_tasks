from rest_framework import viewsets, permissions

from core.models import Task
from core.permissions import ReadOnly
from core.serializers import TaskGetSerializer, TaskCreateSerializer


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated & (ReadOnly | permissions.IsAdminUser)]
    queryset = Task.objects.all()
    lookup_field = 'id'
    
    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TaskGetSerializer
        
        return TaskCreateSerializer
