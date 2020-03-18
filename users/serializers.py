"""
A serializer represents how an object is converted into JSON
"""
from rest_framework import serializers

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    Only username and email are shown
    """

    class Meta:
        model = CustomUser
        #permissions = [
            #("edit_own_playlist_" + models.user.get_username(), "Can edit his own created playlits"),
         #   ("edit_own_playlist", "Can edit his own created playlits"),
        #]
        fields = ['username', 'email', ]
