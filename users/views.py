"""
Define how pages are shown to the user.
Create your views here.
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# Default views for a rest api (with readonly permissions for all users)
from users.models import CustomUser, Playlist
from users.permissions import IsOwnerOrAdmin
from users.serializers import UserSerializer, PlaylistSerializer


class OnlyOwnerViewSet(viewsets.ModelViewSet):
    """
    Base class
    Anyone can view, only the owner can edit
    """

    def get_permissions(self):
        if self.action == 'create':
            # only authenticated users can create
            return [IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            # only owner (or admin) users can modify
            return [IsOwnerOrAdmin()]
        return super(OnlyOwnerViewSet, self).get_permissions()


class UserViewSet(OnlyOwnerViewSet):
    """
    Anyone can view all users, only the owner can edit
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class PlaylistViewSet(OnlyOwnerViewSet):
    """
    Anyone can view all playlists, only the owner can edit
    """
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    def perform_create(self, serializer):
        # sets the current user when creating an object
        serializer.save(user=self.request.user)
