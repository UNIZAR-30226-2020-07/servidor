"""
A serializer represents how an object is converted into JSON
"""
from rest_framework import serializers

from songs.models import Song, Artist, Album


class SongPlainSerializer(serializers.ModelSerializer):
    """
    All fields are shown as plain text
    """

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


class ArtistPlainSerializer(serializers.ModelSerializer):
    """
    All fields are shown as plain text
    """

    class Meta:
        model = Artist
        fields = [
            "id",
            "name",
            "albums",
        ]


class AlbumPlainSerializer(serializers.ModelSerializer):
    """
    All fields are shown as plain text
    """

    class Meta:
        model = Album
        fields = [
            "id",
            "name",
            "songs",
            "artist",
            # "type",
        ]


class ArtistWithAlbums(ArtistPlainSerializer):
    """
    The albums are shown with details
    """
    albums = AlbumPlainSerializer(many=True)


class AlbumWithArtistSerializer(AlbumPlainSerializer):
    """
    The artist is show with details
    """
    artist = ArtistPlainSerializer()


class AlbumWithSongsAndArtistSerializer(AlbumWithArtistSerializer):
    """
    the artist is shown with details and the songs are shown with details
    """
    songs = SongPlainSerializer(many=True)


class SongWithAlbumAndArtistSerializer(SongPlainSerializer):
    """
    Album is shown with details
    """
    album = AlbumWithArtistSerializer()
