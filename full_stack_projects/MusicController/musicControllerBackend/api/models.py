import random, string 

from django.db import models
from django.contrib.auth.models import User


__ROOM_CODE_LENGTH__ = 10


def _generate_random_room_code(length:int=__ROOM_CODE_LENGTH__):    
    while True:
        generated_code = "".join(random.sample(string.ascii_lowercase, length))
    
        try:
            MusicRoom.objects.get(code=generated_code)
        except MusicRoom.DoesNotExist:
            # not sure how efficient this approach this though
            # this means no room with the same code already exists
            return generated_code


# I am currently aware of only 2 methods to set a default method: either a function that accepts no argument
# or something similar to the example given in the serializer_fields api guide: 

class RoomCodeDefaultGenerator:
    """
    May be applied as a `default=...` value on a serializer field.
    returns the current number of rooms created by the user
    """
    requires_context = True
    
    # according to the guide
    # https://www.django-rest-framework.org/api-guide/fields/ (documentation of the 'default' field)
    # the serializer_field argument will include a 'context' field.
    def __call__(self, serializer_field):
        # according to th documentation 
        username = serializer_field.context['username']
        return MusicRoom.objects.filter(host__username=username).count() + 1


class MusicRoom(models.Model):
    code = models.CharField(
                            # primary_key=True, for some reason setting the primary_key to True fucks up a couple of things...
                            max_length=__ROOM_CODE_LENGTH__,  
                            blank=False, 
                            null=False, 
                            unique=True) 

    host = models.ForeignKey(User, 
                             on_delete=models.CASCADE # deleting the user means deleting all the music rooms they created
                             )

    # the number of votes needed to skip the current song played
    votes_to_skip = models.IntegerField(null=False, default=2)

    created_at = models.DateTimeField(auto_now_add=True)

    creation_order = models.IntegerField(null=False, blank=False)

    class Meta:
        ordering = ['creation_order']
