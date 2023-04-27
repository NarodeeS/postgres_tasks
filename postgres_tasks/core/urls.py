from rest_framework import routers

from django.urls import path
from core.viewsets.database_viewset import DatabaseViewSet
from core.viewsets.task_viewset import TaskViewSet

from core.viewsets.email import EmaillApiView


router = routers.DefaultRouter()
router.register('databases', DatabaseViewSet)
router.register('tasks', TaskViewSet, basename='task')

urlpatterns = router.urls

urlpatterns += [
    path('email/verification/', EmaillApiView.as_view()),
]
