"""
A serializer represents how an object is converted into JSON
"""

from rest_framework import serializers

from songs.serializers import SongWithAlbumAndArtistSerializer
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
        read_only = [
            'user'
        ]


class PlaylistWithSongAndAlbumAndArtistSerializer(serializers.ModelSerializer):
    """
    Songs/album/artist are shown with details
    """

    def to_representation(self, instance):
        """
        Shows songs with details, but accepts only id
        """
        representation = super().to_representation(instance)
        if instance.songs is not None:
            representation['songs'] = SongWithAlbumAndArtistSerializer(instance.songs, many=True).data
        return representation

    class Meta:
        model = Playlist
        fields = [
            "id",
            "name",
            "songs",
            "user",
        ]


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


class UserWithPlaylistSerializer(UserPlainSerializer):
    """
    Public information about a user
    """

    def to_representation(self, instance):
        """
        Shows playlists with details, but accepts only id
        """
        representation = super().to_representation(instance)
        if instance.playlists is not None:
            representation['playlists'] = PlaylistPlainSerializer(instance.playlists, many=True).data
        return representation


class UserWithPlaylistSerializer_AUTH(UserWithPlaylistSerializer):
    """
    Public + private information about a user
    """

    def to_representation(self, instance):
        """
        Shows pause_song with details, but accepts only id
        """
        representation = super().to_representation(instance)
        if instance.pause_song is not None:
            representation['pause_song'] = SongWithAlbumAndArtistSerializer(instance.pause_song).data
        return representation

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.fields += [
            "pause_song",
            "pause_second",
        ]


class PlaylistWithUserAndSongAndAlbumAndArtistSerializer(PlaylistWithSongAndAlbumAndArtistSerializer):
    """
    User and songs/album/artist are shown with details
    """

    user = UserPlainSerializer()
