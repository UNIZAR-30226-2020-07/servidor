"""
A serializer represents how an object is converted into JSON
"""
from rest_framework import serializers

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    Only id, username and email is shown
    """

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', ]
