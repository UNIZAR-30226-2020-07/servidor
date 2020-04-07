"""
Manages the admin site with the custom elements.
Register your models here.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Playlist, Valoration

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Playlist)
admin.site.register(Valoration)
