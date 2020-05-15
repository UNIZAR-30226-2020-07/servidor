"""
Define how pages are shown to the user.
Create your views here.
"""
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# Default views for a rest api (with readonly permissions for all users)
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from songs.models import Song
from users.models import CustomUser, Playlist
from users.permissions import IsOwnerOrAdmin
from users.serializers import UserWithPlaylistAndFriendsSerializer, PlaylistWithUserAndSongAndAlbumAndArtistSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    Anyone can view all users, only the owner can edit
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserWithPlaylistAndFriendsSerializer

    search_fields = ['username', 'email']

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            # only owner (or admin) users can modify
            return [IsOwnerOrAdmin()]
        return super().get_permissions()


class PlaylistViewSet(viewsets.ModelViewSet):
    """
    Anyone can view all playlists, only the owner can edit
    """
    queryset = Playlist.objects.all()
    serializer_class = PlaylistWithUserAndSongAndAlbumAndArtistSerializer

    search_fields = ['name']

    @action(methods=['POST'], detail=True, url_path='addSong/(?P<songid>[^/.]+)')
    def addSong(self, request, pk=None, songid=None):
        """
        WebAPI incomplete: POST to add the song with id to this playlist.songs list
        """
        playlist = self.get_object()

        # check permissions
        self.check_object_permissions(request, playlist)

        # check already in list
        if playlist.songs.filter(id=songid).exists():
            return Response({'detail': 'Song already exists'}, HTTP_400_BAD_REQUEST)

        try:
            # check song to add
            song = Song.objects.get(id=songid)
        except Song.DoesNotExist:
            return Response({'detail': 'Invalid song id'}, HTTP_404_NOT_FOUND)

        # add song
        playlist.songs.add(song)

        # return playlist
        return Response(self.get_serializer(playlist).data)

    def perform_create(self, serializer):
        # sets the current user when creating an object
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            # only authenticated users can create
            return [IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy', 'addSong']:
            # only owner (or admin) users can modify
            return [IsOwnerOrAdmin()]
        return super().get_permissions()
