"""
List of models
"""
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from sortedm2m.fields import SortedManyToManyField

from main import settings
from songs.models import Song, Album


class CustomUser(AbstractUser):
    """
    Extends the default user
    """
    # playlists : reverse relation in Playlist
    friends = models.ManyToManyField("self", blank=True, symmetrical=False)
    pause_song = models.ForeignKey(Song, null=True, blank=True, on_delete=models.SET_NULL)
    pause_second = models.PositiveIntegerField(null=True, blank=True)
    albums = models.ManyToManyField(Album, blank=True)
    valorations = models.ManyToManyField(Song, through='Valoration', related_name='user_valorations')


class Playlist(models.Model):
    """
    Object Playlist with title, ID and Songs
    """
    name = models.CharField(max_length=100)
    songs = SortedManyToManyField(Song, blank=True, related_name='playlists')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='playlists')

    def __str__(self):
        return self.name


class Valoration(models.Model):
    """
    Valoration relationship
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    valoration = models.IntegerField(blank=True, null=True, validators=[MaxValueValidator(5), MinValueValidator(1)])

    def __str__(self):
        return f"{self.user}-{self.song}: {self.valoration}"
