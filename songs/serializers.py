"""
A serializer represents how an object is converted into JSON
"""
from rest_framework import serializers

from songs.models import Song, Artist, Album


class SongSerializer(serializers.ModelSerializer):
    """
    All fields are shown
    """

    class Meta:
        model = Song
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    """
    All fields are shown
    songs is a detailed list
    """
    songs = SongSerializer(many=True)  # make songs be a list of songs as json, not just their id

    class Meta:
        model = Album
        fields = '__all__'


class ArtistSerializer(serializers.ModelSerializer):
    """
    All fields are shown
    albums is a detailed list
    """
    albums = AlbumSerializer(many=True)  # make albums be a list of albums as json, not just their id

    class Meta:
        model = Artist
        fields = '__all__'
