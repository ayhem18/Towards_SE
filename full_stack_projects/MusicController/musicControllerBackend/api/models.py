import random, string 

from django.db import models
# Create your models here.

__ROOM_CODE_LENGTH__ = 10


def __generate_random_room_code(length:int=__ROOM_CODE_LENGTH__):
    
    while True:
        generated_code = "".join(random.sample(string.ascii_lowercase, length))
    
        try:
            Room.objects.get(code__exact=generated_code)
        except Room.DoesNotExist:
            # not sure how efficient this approach this though
            # this means no room with the same already exists
            return generated_code
    

class Room(models.Model):
    code = models.CharField(max_length=__ROOM_CODE_LENGTH__, 
                            # set a default value
                            default='', # the default of room code will be generated randomly
                            blank=False, 
                            null=False, 
                            unique=True) 

    # host for the moment is just a string: it is the session key (not sure exactly how these work...)
    host = models.CharField(max_length=50, unique=True)

    guest_can_pause = models.BooleanField(null=False, default=False)

    votes_to_skip = models.IntegerField(null=False, default=2)
        
    created_at = models.DateTimeField(auto_now_add=True)
