"""
Define how pages are shown to the user.
Create your views here.
"""
from rest_framework import viewsets

from songs.models import Song, Artist, Album, Playlist
from songs.serializers import SongSerializer, ArtistSerializer, AlbumSerializer, PlaylistSerializer


# Default views for a rest api (with readonly permissions for all users)
class ArtistViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Artists are readonly
    """
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class AlbumViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Albums are readonly
    """
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class SongViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Songs are readonly
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class PlaylistViewSet(viewsets.ModelViewSet):
    """
    Playlist are readonly
    """
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
