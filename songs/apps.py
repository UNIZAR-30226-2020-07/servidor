"""
Registers this folder as a Django app
"""
from django.apps import AppConfig


class SongsConfig(AppConfig):
    """
    App to manage the songs/album/artist database readonly section
    """
    name = 'songs'
