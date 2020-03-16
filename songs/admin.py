"""
Manages the admin site with the custom elements.
Register your models here.
"""
from django.contrib import admin

from songs.models import Artist, Album, Song, Playlist

admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Playlist)
