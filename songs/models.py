from django.db import models


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
