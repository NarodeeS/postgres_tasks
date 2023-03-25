from rest_framework import viewsets, permissions, authentication

from core.models import UserTask
from core.serializers import UserTaskSerializer
from core.permissions import IsOwner


class UserTasksViewSet(viewsets.ModelViewSet):
    queryset = UserTask.objects.all()
    serializer_class = UserTaskSerializer
    lookup_field = 'id'
    permission_classes = [IsOwner & permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
