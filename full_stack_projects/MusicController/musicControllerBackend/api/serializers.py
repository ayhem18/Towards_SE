from .models import MusicRoom

from rest_framework import serializers as sers
from django.contrib.auth.models import User

class MusicRoomReadSerializer(sers.ModelSerializer):
    class Meta:
        model = MusicRoom
        fields = '__all__'


class MusicRoomWriteSerializer(sers.ModelSerializer):
    host = sers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all()) # so basically the host will be identified by their username

    class Meta:
        model = MusicRoom
        fields = ('host', 'votes_to_skip')

