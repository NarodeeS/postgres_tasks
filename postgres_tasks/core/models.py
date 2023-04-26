from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from .service.database_status import DatabaseStatus
from .managers import UserManager


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    student_group = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    email_confirmed = models.BooleanField(default=False)
    username = models.CharField(
        max_length=150,
        unique=True, 
        blank=True, 
        null=True
    )
    objects = UserManager()

    REQUIRED_FIELDS = ['first_name', 'last_name', 'student_group']
    USERNAME_FIELD = 'email'
    
    def get_db_username(self):
        return self.email.split('@')[0]
    
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    difficulty = models.IntegerField()
    moves_count = models.IntegerField()
    creation_script = models.FileField(upload_to='creation_scripts')
    check_script = models.FileField(upload_to='check_scripts')
    db_structure = models.ImageField(upload_to='dbs_structure')
    
    def __str__(self) -> str:
        return self.title


class CompletedTask(models.Model):
    id = models.AutoField(primary_key=True)
        
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def get_check_script(self):
        return self.task.check_script
    
    def __str__(self) -> str:
        return f"Completed task '{self.task.title}'" \
                "for user '{self.user.username}'"


class DatabaseInfo(models.Model):
    id = models.AutoField(primary_key=True)
    
    db_name = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=10, default=DatabaseStatus.DOWN.value)
    db_password = models.CharField(max_length=10)
    moves_performed = models.IntegerField(default=0)
    last_action_datetime = models.DateTimeField(auto_now=True)
    
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def moves_left(self) -> int:
        return self.task.moves_count - self.moves_performed
    
    def save(self, *args, **kwargs):
        self.last_action_datetime = timezone.now()
        super().save(*args, **kwargs)
    
    def increment_moves(self):
        self.moves_performed += 1
        self.save()

    def __str__(self) -> str:
        return self.db_name
