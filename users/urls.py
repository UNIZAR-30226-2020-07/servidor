"""
Registers in Django the url->view relations
"""
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, PlaylistViewSet

# Create a router and register our viewsets with it.

router = DefaultRouter()
router.register(r'playlist', PlaylistViewSet)
router.register(r'user', UserViewSet)
