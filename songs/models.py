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

# Object Artist with name and list of albums
class Artist(models.Model):
    name = models.CharField(max_length=100)


# Object album with name, artist and list of songs
class Album(models.Model):
    name = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, null=True, on_delete=models.SET_NULL, related_name='albums')


# Object Song with title, duration (seconds), stream_url for future use and album
class Song(models.Model):
    title = models.CharField(max_length=100)
    duration = models.IntegerField()
    stream_url = models.CharField(max_length=100)
    album = models.ForeignKey(Album, null=True, on_delete=models.SET_NULL, related_name='songs')

    genre = models.CharField(
        max_length=14,
        choices=Genre.choices,
    )
