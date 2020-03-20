"""
List of models
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Extends the default user
    """
    # playlist : defined in PlayList Model
    friends = models.ManyToManyField("self")
