"""
Define how pages are shown to the user.
Create your views here.
"""
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated

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

    def perform_create(self, serializer):
        # sets the current user when creating an object
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            # only authenticated users can create
            return [IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            # only owner (or admin) users can modify
            return [IsOwnerOrAdmin()]
        return super(self.__class__, self).get_permissions()


class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to only allow owners or admins of an object to edit it.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or (request.user and request.user.is_staff)
