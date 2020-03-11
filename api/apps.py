"""
Registers this folder as a Django app
"""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """
    App to manage the api elements
    """
    name = 'api'
