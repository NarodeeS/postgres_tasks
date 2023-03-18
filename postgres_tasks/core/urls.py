from django.urls import path
from rest_framework import routers

from core.viewsets.database_viewset import DatabaseViewSet
from core.viewsets.task_viewset import TaskViewSet
from core.viewsets.active_task_viewset import ActiveTaskViewSet

router = routers.DefaultRouter()
router.register('databases', DatabaseViewSet)
router.register('tasks', TaskViewSet)
router.register('active-tasks', ActiveTaskViewSet)

urlpatterns = router.urls
  