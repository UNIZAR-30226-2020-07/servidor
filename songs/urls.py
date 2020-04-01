"""
Registers in Django the url->view relations
"""
from rest_framework.routers import DefaultRouter

from songs.views import ArtistViewSet, AlbumViewSet, SongViewSet

# Create a router and register our viewsets with it.

router = DefaultRouter()
router.register(r'artists', ArtistViewSet)
router.register(r'albums', AlbumViewSet)
router.register(r'songs', SongViewSet)
