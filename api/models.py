from django.db import models
from django.db.models.base import Model

# Create your models here.


class UserModel(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
