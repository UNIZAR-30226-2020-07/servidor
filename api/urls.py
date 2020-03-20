"""
Registers in Django the url->view relations
"""
from django.conf.urls import url
from django.urls import include, path

from api.views import schema_view

urlpatterns = [
    path('', include('songs.urls')),  # consider using a subpath
    path('', include('users.urls')),  # to avoid clasing

    # for the swagger views
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api-auth/', include('rest_framework.urls')),  # for webapi session auth

]
