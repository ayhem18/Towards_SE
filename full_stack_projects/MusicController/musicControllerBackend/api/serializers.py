from typing import Any
from rest_framework import serializers as sers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

from .models import MusicRoom, __ROOM_CODE_LENGTH__, _generate_random_room_code, RoomCodeDefaultGenerator


class MusicRoomReadSerializer(sers.ModelSerializer):
    # serialize the user using his username, instead of id (the default)
    host = sers.SlugRelatedField(many=False, 
                                 slug_field='username', 
                                 queryset=User.objects.all()) # so basically the host will be identified by their username

    code = sers.CharField(write_only=True) # the code should not appear when returning the room information

    class Meta:
        model = MusicRoom
        # fields = '__all__'
        exclude = ['id']

        
class MusicRoomWriteSerializer(sers.ModelSerializer):

    host = sers.SlugRelatedField(many=False, 
                                 slug_field='username', # so basically the host will be identified by their username
                                 queryset=User.objects.all() 
                                 ) 

    code = sers.CharField(max_length=__ROOM_CODE_LENGTH__,
                          default=_generate_random_room_code, # the default generation function is designed to satisfy uniqueness 
                          validators=[
                              UniqueValidator(queryset=MusicRoom.objects.all()) # if the code was passed by the user, it has to be unique
                              ],
                          required=False
                        )

    creation_order = sers.IntegerField(default=RoomCodeDefaultGenerator(), # make sure to pass an instance of the class and not the class itself
                                       required=False)
    
    class Meta:
        model = MusicRoom
        fields = ('host', 'votes_to_skip', 'code', 'creation_order')

