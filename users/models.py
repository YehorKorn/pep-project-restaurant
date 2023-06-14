from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class User(AbstractUser):

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        db_table = "main_user"   #

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"
