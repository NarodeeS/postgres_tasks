from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response

from core.models import UserTask
from core.serializers import UserTaskSerializer
from core.permissions import IsOwner


class UserTasksViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin, 
                       viewsets.GenericViewSet):
    queryset = UserTask.objects.all()
    serializer_class = UserTaskSerializer
    lookup_field = 'id'
    permission_classes = [IsOwner & permissions.IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        task_id = request.data['task']
        if UserTask.objects.filter(task__id=task_id).exists():
            return Response(data={'error': 'Such task already assigned to this user'})
        return super().create(request, *args, **kwargs)
