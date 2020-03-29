"""
A serializer represents how an object is converted into JSON
"""

from rest_framework import serializers

from songs.serializers import SongWithAlbumAndArtistSerializer
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
    Songs/album/artist are shown with details
    """
    songs = ShowDetailsAcceptPkField(SongWithAlbumAndArtistSerializer, many=True)


class UserPlainSerializer(serializers.ModelSerializer):
    """
    User information plain
    """

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "playlists",
            "friends",
        ]


class UserWithPlaylistAndFriendsSerializer(UserPlainSerializer):
    """
    Public information about a user
    """

    playlists = ShowDetailsAcceptPkField(PlaylistPlainSerializer, many=True)
    friends = ShowDetailsAcceptPkField(UserPlainSerializer, many=True)


class UserAuthSerializer(UserWithPlaylistAndFriendsSerializer):
    """
    Public + private information about a user
    """

    pause_song = ShowDetailsAcceptPkField(SongWithAlbumAndArtistSerializer)

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
    User and songs/album/artist are shown with details
    """

    user = UserPlainSerializer(read_only=True)
