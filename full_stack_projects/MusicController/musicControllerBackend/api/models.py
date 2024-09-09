import random, string 

from django.db import models
from django.contrib.auth.models import User

__ROOM_CODE_LENGTH__ = 10

def __generate_random_room_code(length:int=__ROOM_CODE_LENGTH__):    
    while True:
        generated_code = "".join(random.sample(string.ascii_lowercase, length))
    
        try:
            MusicRoom.objects.get(code__exact=generated_code)
        except MusicRoom.DoesNotExist:
            # not sure how efficient this approach this though
            # this means no room with the same already exists
            return generated_code
    


class MusicRoom(models.Model):
    code = models.CharField(max_length=__ROOM_CODE_LENGTH__,
                            # set a default value
                            default='', # the default of room code will be generated randomly
                            blank=False, 
                            null=False, 
                            unique=True) 

    # the number of votes needed to 
    votes_to_skip = models.IntegerField(null=False, default=2)

    created_at = models.DateTimeField(auto_now_add=True)

    host = models.ForeignKey(User, 
                             on_delete=models.CASCADE # deleting the user means deleting all the music rooms they created
                             )

