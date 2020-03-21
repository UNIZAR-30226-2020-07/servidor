"""
Registers in Django the url->view relations
"""
from rest_framework.routers import DefaultRouter

from songs.views import ArtistViewSet, AlbumViewSet, SongViewSet

# Create a router and register our viewsets with it.

router = DefaultRouter()
router.register(r'artist', ArtistViewSet)
router.register(r'album', AlbumViewSet)
router.register(r'songs', SongViewSet)  # TODO: change to singular 'song'
