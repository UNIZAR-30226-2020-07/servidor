from rest_framework.permissions import BasePermission

from users.models import CustomUser


class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to only allow owners or admins of an object to edit it.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return self.getUser(obj) == request.user or (request.user and request.user.is_staff)

    def getUser(self, obj):
        model = type(obj)
        if model is CustomUser:
            return obj
        else:
            return obj.user
