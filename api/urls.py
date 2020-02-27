from django.urls import include, path

urlpatterns = [
    path('', include('songs.urls')),
    path('', include('users.urls')),
]
