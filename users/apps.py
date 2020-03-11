"""
Registers this folder as a Django app
"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    App to manage the users (authentication, model, etc)
    """
    name = 'users'
