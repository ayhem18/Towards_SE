from django.db import models

from django.contrib.auth.models import User


class UserSpotifyCredentials(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    # # the authorization code is requested once to acess both the access and refresh token from spotify
    # authorization_code = models.CharField(max_length=100, null=False)

    # the refresh token is used to request a new access token since the access token expires after a certain period of time
    refresh_token = models.CharField(max_length=100, null=False)

    # the access token is the actual credentials needed to access the user's music
    current_access_token = models.CharField(max_length=100, null=False)

    class Meta:
        # order the credentials by their username
        ordering = ['user__username']
        
    
class SpotifyAuthorizationAccess(models.Model):

    client_id = models.CharField(max_length=100, null=False, unique=True)
    client_secret = models.CharField(max_length=100, null=False, unique=True)
    authorization_code = models.CharField(max_length=100, null=False) 

    class Meta:
        # save a new spotify authorization code whenever the secrete key changes (in case it was compromised)
        unique_together = ['client_id', 'client_secret']


