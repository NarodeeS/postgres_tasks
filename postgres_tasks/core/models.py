from django.db import models
from django.contrib.auth.models import User

from .utils.database_status import DatabaseStatus


class DatabaseInfo(models.Model):
    db_name = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=10, default=DatabaseStatus.DOWN.value)

    def __str__(self) -> str:
        return self.db_name
