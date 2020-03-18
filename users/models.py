"""
List of models
"""
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Extends the default user
    """
    friends = models.ManyToManyField("self")


# https://docs.djangoproject.com/en/3.0/topics/auth/customizing/
class MyBackend(BaseBackend):
    """
    Extends the default BaseBackend
    """

    @staticmethod
    def has_perm_edit_playlist(user_obj, playlist_obj):
        return user_obj.username == playlist_obj.owner.username
