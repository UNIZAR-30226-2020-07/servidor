"""
List of models
"""
from django.contrib.auth.models import AbstractUser
from django.db import models

from main import settings
from songs.models import Song


class CustomUser(AbstractUser):
    """
    Extends the default user
    """
    # playlists : reverse relation in Playlist
    friends = models.ManyToManyField("self")


class Playlist(models.Model):
    """
    Object Playlist with title, ID and Songs
    """
    name = models.CharField(max_length=100)
    songs = models.ManyToManyField(Song, related_name='playlists')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='playlists')

    def __str__(self):
        return self.name
