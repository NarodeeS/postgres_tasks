from rest_framework import viewsets

from core.models import UserTask
from core.serializers import UserTaskSerializer


class UserTasksViewSet(viewsets.ReadOnlyModelViewSet):
    # get only user tasks
    queryset = UserTask.objects.all()
    serializer_class = UserTaskSerializer
    lookup_field = 'id'
