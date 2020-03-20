"""
Registers in Django the url->view relations
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from songs.views import ArtistViewSet, AlbumViewSet, SongViewSet, PlaylistViewSet
from users.views import UserViewSet

# Create a router and register our viewsets with it.

router = DefaultRouter()
router.register(r'artist', ArtistViewSet)
router.register(r'album', AlbumViewSet)
router.register(r'songs', SongViewSet)
router.register(r'playlist', PlaylistViewSet)
router.register(r'user', UserViewSet)

# The API URLs are determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
