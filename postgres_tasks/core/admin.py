from django.contrib import admin

from .models import DatabaseInfo, Task, CompletedTask, User


admin.site.register((User, DatabaseInfo, Task, CompletedTask))
