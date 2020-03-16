"""
List of models
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Extends the default user
    """
    friends = models.ManyToManyField('CustomUser')
    pass
