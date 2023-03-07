from django.urls import path

from core import views


urlpatterns = [
    path('', views.HomeView.as_view()),
    path('db/', views.DbViewCreate.as_view()),
    path('db/<str:db_name>/', views.DbViewGetDelete.as_view())
]
