from django.contrib import admin

# Register your models here.

from .models import SpotifyAuthCode, UserSpotifyCredentials

admin.site.register(SpotifyAuthCode)
admin.site.register(UserSpotifyCredentials)

