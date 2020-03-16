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
        fields = ['username', 'email', 'friends', ]
