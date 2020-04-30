"""
A serializer represents how an object is converted into JSON
"""
from django.db.models import Avg, Count
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from songs.fields import ValorationField
from songs.models import Song, Artist, Album
from users.models import Valoration


class SongPlainSerializer(serializers.ModelSerializer):
    """
    All fields are shown as plain text
    """

    user_valoration = ValorationField()
    avg_valoration = SerializerMethodField()
    count_valoration = SerializerMethodField()

    def get_avg_valoration(self, song):
        """
        Average valoration of all users
        """
        return Valoration.objects.filter(song=song).aggregate(avg=Avg('valoration'))['avg']

    def get_count_valoration(self, song):
        """
        Average valoration of all users
        """
        return Valoration.objects.filter(song=song).aggregate(count=Count('valoration'))['count']

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
            "avg_valoration",
            "count_valoration",
            "created_at",
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
