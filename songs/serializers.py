"""
A serializer represents how an object is converted into JSON
"""
from rest_framework import serializers

from songs.models import Song, Artist, Album, Playlist


class ArtistSerializer(serializers.ModelSerializer):
    """
    All fields are shown
    """

    # albums = AlbumSerializer(many=True)  # make albums be a list of albums as json, not just their id

    class Meta:
        model = Artist
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    """
    All fields are shown
    """
    # songs = SongSerializer(many=True)  # make songs be a list of songs as json, not just their id
    artist = ArtistSerializer()

    class Meta:
        model = Album
        fields = '__all__'


class SongSerializer(serializers.ModelSerializer):
    """
    All fields are shown
    """

    album = AlbumSerializer()

    class Meta:
        model = Song
        fields = '__all__'


class PlaylistSerializer(serializers.ModelSerializer):
    """
    All fields are shown
    """

    class Meta:
        model = Playlist
        fields = '__all__'
