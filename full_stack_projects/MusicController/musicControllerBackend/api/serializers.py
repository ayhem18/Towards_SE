from .models import Room

from rest_framework.serializers import ModelSerializer

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        depth = 1


class CreateRoomSerializer(ModelSerializer):
    class Meta:
        model=Room
        fields = ('guest_can_pause', 'votes_to_skip')
        
