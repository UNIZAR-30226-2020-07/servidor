"""
Registers this folder as a Django app
"""
from django.apps import AppConfig


class SongsConfig(AppConfig):
    """
    App for the readonly part of the database
    TODO: rename to readonly
    """
    name = 'songs'
