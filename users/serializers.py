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
        exclude = (  # exclude internal data
            "password",
            "last_login",
            "is_superuser",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "date_joined",
            "groups",
            "user_permissions",
        )
