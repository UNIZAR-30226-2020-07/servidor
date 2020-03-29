"""
Define how pages are shown to the user.
Create your views here.
"""
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

# Default views for a rest api (with readonly permissions for all users)
from users.models import CustomUser, Playlist
from users.permissions import IsOwnerOrAdmin
from users.serializers import UserWithPlaylistAndFriendsSerializer, PlaylistWithUserAndSongAndAlbumAndArtistSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    Anyone can view all users, only the owner can edit
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserWithPlaylistAndFriendsSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            # only owner (or admin) users can modify
            return [IsOwnerOrAdmin()]
        return super().get_permissions()


class PlaylistViewSet(viewsets.ModelViewSet):
    """
    Anyone can view all playlists, only the owner can edit
    """
    queryset = Playlist.objects.all()
    serializer_class = PlaylistWithUserAndSongAndAlbumAndArtistSerializer

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
        return super().get_permissions()
