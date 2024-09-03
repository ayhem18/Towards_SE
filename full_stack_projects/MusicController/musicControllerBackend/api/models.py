from django.db import models

# Create your models here.

__ROOM_CODE_LENGTH__ = 10

class Room(models.Model):
    code = models.CharField(max_length=__ROOM_CODE_LENGTH__, 
                            blank=False, 
                            null=False, 
                            unique=True)

    # host for the moment is just a string
    host = models.CharField(max_length=50, unique=True)

    guest_can_pause = models.BooleanField(null=False, default=False)

    votes_to_skip = models.IntegerField(null=False, default=2)
        
    created_at = models.DateTimeField(auto_now_add=True)
