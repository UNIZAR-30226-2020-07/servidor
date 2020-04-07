"""
List of models
"""
from django.core.exceptions import ValidationError
from django.db import models


class Genre(models.TextChoices):
    NINETYS = "90s"
    CLASSIC = "Classic"
    ELECTRONIC = "Electronic"
    REGGAE = "Reggae"
    R_B = "R&B"
    LATIN = "Latin"
    OLDIES = "Oldies"
    COUNTRY = "Country"
    RAP = "Rap"
    ROCK = "Rock"
    METAL = "Metal"
    POP = "Pop"
    BLUES = "Blues"
    JAZZ = "Jazz"
    FOLK = "Folk"
    EIGHTYS = "80s"


##############################

class Artist(models.Model):
    """
    Object Artist with name and list of albums
    """
    name = models.CharField(max_length=100)

    # albums = reverse relation in Album

    def __str__(self):
        return self.name


class Album(models.Model):
    """
    Object album with name, artist and list of songs
    """
    name = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, null=True, on_delete=models.SET_NULL, related_name='albums')
    podcast = models.BooleanField(default=False)

    # songs = reverse relation in Song

    def __str__(self):
        return self.name


class Song(models.Model):
    """
    Object Song with title, duration (seconds), stream_url for future use and album
    """
    title = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()
    stream_url = models.CharField(max_length=100)
    album = models.ForeignKey(Album, null=True, on_delete=models.SET_NULL, related_name='songs')
    genre = models.CharField(
        max_length=max(len(e) for e in Genre.__members__.values()),  # automatic max length
        choices=Genre.choices,
    )
    episode = models.BooleanField(default=False)

    # playlists: reverse relation in Playlist
    # user_valoration: reverse relation in User

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # Allow episodes only on podcasts and viceversa
        if self.episode != self.album.podcast:
            raise ValidationError('An episode can only be in a podcast' if self.episode else "A song can't be in a podcast")
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def __str__(self):
        return self.title
