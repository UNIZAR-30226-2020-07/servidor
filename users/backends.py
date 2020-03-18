from django.contrib.auth.backends import BaseBackend


# https://docs.djangoproject.com/en/3.0/topics/auth/customizing/
class MyBackend(BaseBackend):
    """
    Extends the default BaseBackend
    """

    @staticmethod
    def has_perm_edit_playlist(user_obj, playlist_obj):
        return user_obj.username == playlist_obj.owner.username
