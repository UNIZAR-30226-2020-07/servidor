"""
A serializer represents how an object is converted into JSON
"""
from rest_framework import serializers

from songs.models import Song, Artist, Album


class ArtistSerializer(serializers.ModelSerializer):
    """
    All fields are shown
    """

    class Meta:
        model = Artist
        fields = [
            "id",
            "name",
            "albums",
        ]


class AlbumSerializer(serializers.ModelSerializer):
    """
    All fields are shown
    """
    artist = ArtistSerializer()

    class Meta:
        model = Album
        fields = [
            "id",
            "name",
            "songs",
            "artist",
            # "type",
        ]


class SongSerializer(serializers.ModelSerializer):
    """
    All fields are shown
    """

    album = AlbumSerializer()

    class Meta:
        model = Song
        fields = [
            "id",
            "title",
            "duration",
            "stream_url",
            "album",
            "genre",
        ]
