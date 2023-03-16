from rest_framework import viewsets

from core.models import Task
from core.serializers import TaskSerializer


class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'
