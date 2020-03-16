"""
List of models
"""
from django.db import models


class Genre(models.TextChoices):
    NINETYS = "90s"
    CLASSIC = "Classic"
    ELECTRONIC = "Electronic"
    REGGAE = "Reggase"
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

    PLAYLIST = "Playlist"


##############################

class Artist(models.Model):
    """
    Object Artist with name and list of albums
    """
    name = models.CharField(max_length=100)

    # albums = reverse relation

    def __str__(self):
        return self.name


class Album(models.Model):
    """
    Object album with name, artist and list of songs
    """
    name = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, null=True, on_delete=models.SET_NULL, related_name='albums')

    # songs = reverse relation

    def __str__(self):
        return self.name


class Song(models.Model):
    """
    Object Song with title, duration (seconds), stream_url for future use and album
    """
    title = models.CharField(max_length=100)
    duration = models.IntegerField()
    stream_url = models.CharField(max_length=100)
    album = models.ForeignKey(Album, null=True, on_delete=models.SET_NULL, related_name='songs')
    genre = models.CharField(
        max_length=max(len(e) for e in Genre.__members__.values()),  # automatic max length
        choices=Genre.choices,
    )

    def __str__(self):
        return self.title


class Playlist(models.Model):
    """
    Object Playlist with title, ID and Songs
    """
    name = models.CharField(max_length=100)
    allSongs = models.ForeignKey(Song, null=True, on_delete=models.SET_NULL, related_name='playlists')

    def __str__(self):
        return self.name
