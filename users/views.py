"""
Define how pages are shown to the user.
Create your views here.
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from songs.permissions import IsOwnerOrAdmin
# Default views for a rest api (with readonly permissions for all users)
from users.models import CustomUser
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Artists are readonly
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            # only authenticated users can create
            return [IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            # only owner (or admin) users can modify
            return [IsOwnerOrAdmin()]
        return super(self.__class__, self).get_permissions()
