from django.contrib import admin

from .models import DatabaseInfo, Task, ActiveTask, UserTask


admin.site.register(DatabaseInfo)
admin.site.register(Task)
admin.site.register(ActiveTask)
admin.site.register(UserTask)
