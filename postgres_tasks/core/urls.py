from rest_framework import routers

from core.viewsets.database_viewset import DatabaseViewSet
from core.viewsets.task_viewset import TaskViewSet


router = routers.DefaultRouter()
router.register('databases', DatabaseViewSet)
router.register('tasks', TaskViewSet, basename='task')

urlpatterns = router.urls
