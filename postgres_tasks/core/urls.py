from django.urls import path
from rest_framework import routers

from core.views import db_views
from core.viewsets.task_viewset import TaskViewSet
from core.viewsets.active_task_viewset import ActiveTaskViewSet

router = routers.DefaultRouter()
router.register('tasks', TaskViewSet)
router.register('active-tasks', ActiveTaskViewSet)


urlpatterns = [
    path('databases/', db_views.DbCreateView.as_view()),
    path('databases/<str:db_name>/', db_views.DbGetDeleteView.as_view()),
    path('databases/<str:db_name>/command/', db_views.DbCommandView.as_view()),
    path('databases/<str:db_name>/check/', db_views.DbCheckView.as_view()),
]

urlpatterns += router.urls
  