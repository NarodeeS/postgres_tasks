from rest_framework import viewsets

from core.models import ActiveTask
from core.serializers import ActiveTaskSerializer


class ActiveTaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActiveTask.objects.all()
    serializer_class = ActiveTaskSerializer
    lookup_field = 'id'
