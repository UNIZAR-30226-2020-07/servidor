"""
A serializer represents how an object is converted into JSON
"""
from rest_framework import serializers

from songs.models import Song, Artist, Album


def all_fields(model):
    """
    Utility to add all fields
    When using '__all__' related fields are not included
    """
    return list(f.name for f in model._meta.get_fields())


class ArtistSerializer(serializers.ModelSerializer):
    """
    All fields are shown
    """

    class Meta:
        model = Artist
        fields = all_fields(model)


class AlbumSerializer(serializers.ModelSerializer):
    """
    All fields are shown
    """
    artist = ArtistSerializer()

    class Meta:
        model = Album
        fields = all_fields(model)


class SongSerializer(serializers.ModelSerializer):
    """
    All fields are shown
    """

    album = AlbumSerializer()

    class Meta:
        model = Song
        fields = '__all__'
