"""
A serializer represents how an object is converted into JSON
"""
from rest_framework import serializers

from songs.fields import ValorationField
from songs.models import Song, Artist, Album


class SongPlainSerializer(serializers.ModelSerializer):
    """
    All fields are shown as plain text
    """

    user_valoration = ValorationField()

    class Meta:
        model = Song
        read_only_fields = [
            "id",
            "title",
            "duration",
            "stream_url",
            "album",
            "genre",
            "episode",
        ]
        fields = read_only_fields + [
            "user_valoration",  # the writable field
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
            "podcast",
        ]


class ArtistWithAlbums(ArtistPlainSerializer):
    """
    albums is serialized as plain
    """
    albums = AlbumPlainSerializer(many=True)


class AlbumWithArtistSerializer(AlbumPlainSerializer):
    """
    artist is serialized as plain
    """
    artist = ArtistPlainSerializer()


class AlbumWithSongsAndArtistSerializer(AlbumWithArtistSerializer):
    """
    artist is serialized as plain
    songs is serialized as plain
    """
    songs = SongPlainSerializer(many=True)


class SongWithAlbumAndArtistSerializer(SongPlainSerializer):
    """
    albums is serialized with artist serialized as plain
    """
    album = AlbumWithArtistSerializer(read_only=True)
