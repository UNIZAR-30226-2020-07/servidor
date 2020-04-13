"""
Define how pages are shown to the user.
Create your views here.
"""
from random import sample

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from songs.models import Song, Artist, Album
from songs.search import SongSearch
from songs.serializers import AlbumWithSongsAndArtistSerializer, ArtistWithAlbums, SongWithAlbumAndArtistSerializer
# Default views for a rest api (with readonly permissions for all users)
from users.models import Valoration


class ArtistViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List of artists
    """
    queryset = Artist.objects.all()
    serializer_class = ArtistWithAlbums

    search_fields = ['name']


class AlbumViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List of albums
    """
    queryset = Album.objects.all()
    serializer_class = AlbumWithSongsAndArtistSerializer

    search_fields = ['name']
    filterset_fields = ['podcast']


class SongViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    """
    List of songs
    Includes the current user valoration which can be edited
    """

    queryset = Song.objects.all()
    serializer_class = SongWithAlbumAndArtistSerializer

    filter_backends = [DjangoFilterBackend, SongSearch, ]
    filterset_fields = ['episode']

    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        """
        The user_valoration field should be saved differently
        """
        Valoration.objects.update_or_create(
            user_id=self.request.user.id,
            song_id=serializer.instance.id,
            defaults={'valoration': serializer.validated_data['user_valoration']},
        )

        serializer.data['user_valoration'] = serializer.validated_data['user_valoration']

    @action(detail=False, filter_backends=[])
    def recommended(self, request):
        # self.request.user.is_authenticated

        # consider creating real recommendations, for now just return random ones
        n = 25
        ids = sample(list(Song.objects.values_list('id', flat=True)), n)
        recommendations = Song.objects.filter(id__in=ids).order_by('?')

        page = self.paginate_queryset(recommendations)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recommendations, many=True)
        return Response(serializer.data)
