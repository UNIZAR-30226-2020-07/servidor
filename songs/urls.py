"""
Registers in Django the url->view relations
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from songs import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'artist', views.ArtistViewSet)
router.register(r'album', views.AlbumViewSet)
router.register(r'songs', views.SongViewSet)
router.register(r'playlist', views.PlaylistViewSet)

# The API URLs are determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
