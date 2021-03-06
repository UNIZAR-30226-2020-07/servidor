"""
Registers in Django the url->view relations
"""
from django.conf.urls import url
from django.urls import include, path

from api import routers
from api.views import schema_view, MyUserDetailsView
from songs.urls import router as router_songs
from users.urls import router as router_users

router = routers.DefaultRouter()

# add from other routers
router.extend(router_songs)
router.extend(router_users)

# add custom urls
router.addCustomUrl('login', 'rest_login')
router.addCustomUrl('logout', 'rest_logout')
router.addCustomUrl('register', 'rest_register')
router.addCustomUrl('you', 'my_rest_user_details')
router.addCustomUrl('change_password', 'rest_password_change')
router.addCustomUrl('reset_password', 'rest_password_reset')
router.addCustomUrl('WEB reset_password', 'password_reset')

urlpatterns = [
    path('', include(router.urls)),

    # for authentication
    url(r'^rest-auth/user', MyUserDetailsView.as_view(), name='my_rest_user_details'),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

    # for the swagger views
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # for webapi session auth
    path('api-auth/', include('rest_framework.urls')),

]
