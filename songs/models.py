from django.db import models


# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=100)


class Album(models.Model):
    name = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, null=True, on_delete=models.SET_NULL, related_name='albums')


class Song(models.Model):
    title = models.CharField(max_length=100)
    duration = models.IntegerField()
    stream_url = models.CharField(max_length=100)
    album = models.ForeignKey(Album, null=True, on_delete=models.SET_NULL, related_name='songs')
