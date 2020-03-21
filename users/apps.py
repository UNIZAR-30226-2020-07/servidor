"""
Registers this folder as a Django app
"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    App for the 'anyone can edit, only the owner can edit' part of the database
    TODO: rename to owner_only
    """
    name = 'users'
