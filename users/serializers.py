"""
A serializer represents how an object is converted into JSON
"""

from rest_framework import serializers

from users.models import CustomUser, Playlist


class UserSerializer_API(serializers.ModelSerializer):
    """
    You can edit only the playlists and friends
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
        read_only_fields = ["username", "email"]


class UserSerializer_AUTH(serializers.ModelSerializer):
    """
    You can edit only username and email
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
        read_only_fields = ["playlists", "friends"]


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
