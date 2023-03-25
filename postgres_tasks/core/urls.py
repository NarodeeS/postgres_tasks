from rest_framework import routers

from core.viewsets.database_viewset import DatabaseViewSet
from core.viewsets.task_viewset import TaskViewSet
from core.viewsets.user_tasks_viewset import UserTasksViewSet


router = routers.DefaultRouter()
router.register('databases', DatabaseViewSet)
router.register('tasks', TaskViewSet)
router.register('user-tasks', UserTasksViewSet)

urlpatterns = router.urls
