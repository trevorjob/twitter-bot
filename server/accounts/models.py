# from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid import uuid4


# Create your models here.
class User(AbstractUser):
    id = models.CharField(max_length=50, primary_key=True, default=str(uuid4()))
    refresh_token = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.id
