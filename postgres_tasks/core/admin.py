from django.contrib import admin

from .models import DatabaseInfo, Task, CompletedTask, User


admin.site.register(User)
admin.site.register(DatabaseInfo)
admin.site.register(Task)
admin.site.register(CompletedTask)
