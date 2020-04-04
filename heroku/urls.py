"""
Registers in Django the url->view relations
"""
from django.urls import path

from heroku import views

urlpatterns = [
    path('', views.webhook)
]
