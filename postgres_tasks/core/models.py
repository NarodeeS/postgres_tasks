from django.db import models
from django.utils.timezone import now

from .utils.database_status import DatabaseStatus


class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    difficulty = models.IntegerField()
    creation_script = models.FileField(upload_to='creation_scripts')
    check_script = models.FileField(upload_to='check_scripts')
    db_structure = models.ImageField(upload_to='dbs_structure')
    
    def __str__(self) -> str:
        return self.title
    

class ActiveTask(models.Model):
    deadline = models.DateTimeField(default=now())
    
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f'{self.task.title} ({self.deadline.date()})'


class UserTask(models.Model):
    completed = models.BooleanField(default=False)
    
    active_task = models.ForeignKey(ActiveTask, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.active_task.task.title


class DatabaseInfo(models.Model):
    db_name = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=10, default=DatabaseStatus.DOWN.value)
    
    user_task = models.ForeignKey(UserTask, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.db_name
