from rest_framework import serializers as sers

from .models import UserSpotifyCredentials

class SucReadSerializer(sers.ModelSerializer):
    class Meta:
        model = UserSpotifyCredentials
        fields = '__all__'

# not sure if this is actually a good idea, but at least experimenting with serializers a bit further..

class SucUpdateSerializer(sers.ModelSerializer):
    class Meta:
        model = UserSpotifyCredentials
        fields = '__all__'

    # override the refreshtoken to make it read only and not write
    # the refresh token is set once and cannot be rewritten 
    refresh_token = sers.CharField(read_only=True)
