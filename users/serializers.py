"""
A serializer represents how an object is converted into JSON
"""

from rest_framework import serializers

from songs.serializers import SongSerializer
from users.models import CustomUser, Playlist


class UserSerializer_API(serializers.ModelSerializer):
    """
    Public information about a user
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


class UserSerializer_AUTH(serializers.ModelSerializer):
    """
    Public + private information about a user
    """

    def to_representation(self, instance):
        """
        Shows pause_song with details, but accepts only id
        """
        representation = super(self.__class__, self).to_representation(instance)
        if instance.pause_song is not None:
            representation['pause_song'] = SongSerializer(instance.pause_song).data
        return representation

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


class PlaylistSerializer(serializers.ModelSerializer):
    """
    All fields are shown
    """

    user = UserSerializer_API(read_only=True)  # show user details, and also don't enter when creating

    class Meta:
        model = Playlist
        fields = [
            "id",
            "name",
            "songs",
            "user",
        ]
