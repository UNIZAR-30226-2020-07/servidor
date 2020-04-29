"""
A serializer represents how an object is converted into JSON
"""

from rest_framework import serializers

from songs.serializers import SongWithAlbumAndArtistSerializer, AlbumPlainSerializer
from users.fields import ShowDetailsAcceptPkField
from users.models import CustomUser, Playlist


class PlaylistPlainSerializer(serializers.ModelSerializer):
    """
    All fields are shown as plain text
    """

    class Meta:
        model = Playlist
        fields = [
            "id",
            "name",
            "songs",
            "user",
        ]


class PlaylistWithSongAndAlbumAndArtistSerializer(PlaylistPlainSerializer):
    """
    songs is serialized with albums serialized with artist serialized as plain
    """
    songs = ShowDetailsAcceptPkField(SongWithAlbumAndArtistSerializer, many=True)


class UserPlainSerializer(serializers.ModelSerializer):
    """
    All fields are shown as plain text
    """

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "playlists",
            "friends",
            "albums",
        ]


class UserWithPlaylistAndFriendsSerializer(UserPlainSerializer):
    """
    Public information about a user

    playlists is serializer as plain
    friends is serializer as plain
    albums is serializer as plain
    """

    playlists = ShowDetailsAcceptPkField(PlaylistPlainSerializer, many=True, read_only=True)
    friends = ShowDetailsAcceptPkField(UserPlainSerializer, many=True)
    albums = ShowDetailsAcceptPkField(AlbumPlainSerializer, many=True)


class UserAuthSerializer(UserWithPlaylistAndFriendsSerializer):
    """
    Public + private information about a user

    playlists is serializer as plain
    friends is serializer as plain
    albums is serializer as plain
    pause_song is serializer with albums serialized with artist serialized as plain
    """

    pause_song = ShowDetailsAcceptPkField(SongWithAlbumAndArtistSerializer, allow_null=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "playlists",
            "friends",
            "pause_song",
            "pause_second",
        ]


class PlaylistWithUserAndSongAndAlbumAndArtistSerializer(PlaylistWithSongAndAlbumAndArtistSerializer):
    """
    songs is serialized with albums serialized with artist serialized as plain
    user is serialized as plain
    """

    user = UserPlainSerializer(read_only=True)
