"""
A serializer represents how an object is converted into JSON
"""

from rest_framework import serializers

from users.models import CustomUser, Playlist


def all_fields_except(model, exclude):
    """
    Utility to add all fields except some
    When using 'exclude' related fields are not included
    """
    return list(f.name for f in model._meta.get_fields() if f.name not in exclude)


class UserSerializer(serializers.ModelSerializer):
    """
    Only username and email are shown
    """

    class Meta:
        model = CustomUser
        fields = all_fields_except(model,
                                   (  # exclude internal data
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
                                       "logentry",
                                       "emailaddress",
                                       "auth_token",
                                   ))


class PlaylistSerializer(serializers.ModelSerializer):
    """
    All fields are shown
    """

    user = UserSerializer(read_only=True)  # show user details, and also don't enter when creating

    class Meta:
        model = Playlist
        fields = '__all__'
