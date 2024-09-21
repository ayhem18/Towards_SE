from rest_framework import serializers as sers

from django.contrib.auth.models import User
from .models import YoutubeAuthCode, YoutubeUserCredentials


class YucReadSerializer(sers.ModelSerializer):
    user = sers.SlugRelatedField(many=False, 
                                 slug_field='username', 
                                 queryset=User.objects.all()) # so basically the host will be identified by their username
    class Meta:
        model = YoutubeUserCredentials
        fields = '__all__'

# not sure if this is actually a good idea, but at least experimenting with serializers a bit further..

class YucUpdateSerializer(sers.ModelSerializer):
    class Meta:
        model = YoutubeUserCredentials
        fields = '__all__'

    # override the refreshtoken to make it read only and not write
    # the refresh token is set once and cannot be rewritten 
    refresh_token = sers.CharField(read_only=True)



class YtAuthCodeSerializer(sers.ModelSerializer):
    # override the    
    client_id = sers.CharField(write_only=True)
    client_secret = sers.CharField(write_only=True)

    class Meta:
        model = YoutubeAuthCode
        fields = '__all__'
