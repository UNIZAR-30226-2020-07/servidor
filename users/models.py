"""
List of models
"""
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Extends the default user
    """
    pass
