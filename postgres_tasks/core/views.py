from django.shortcuts import render
from django import views
from django.http import HttpRequest, HttpResponse


class HomeView(views.View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'core/index.html')
