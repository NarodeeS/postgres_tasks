from django.urls import path

from core import views


urlpatterns = [
    path('', views.HomeView.as_view()),
    path('db/', views.DbCreateView.as_view()),
    path('db/<str:db_name>/', views.DbGetDeleteView.as_view()),
    path('db/<str:db_name>/command/', views.DbCommandView.as_view()),
    path('db/<str:db_name>/check/', views.DbCheckView.as_view()),
]
