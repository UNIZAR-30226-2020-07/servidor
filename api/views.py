from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Create your views here.

# Swagger views
schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
        description="Test version of the api",
        # terms_of_service="none",
        # contact=openapi.Contact(email="none"),
        # license=openapi.License(name="none"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
