# we will use the requests package to send requests to the spotify authentication server
import requests as rq

from django.shortcuts import render

from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import status as st

from .credentials import CLIENT_ID, API_SCOPES, USER_AUTH_REDIRECT_URI, CLIENT_SECRET    
from .serializers import SucReadSerializer, SucUpdateSerializer

# since we will use the authorization of the user once...
# then the authorization code flow is the most suitable: 
# https://developer.spotify.com/documentation/web-api/tutorials/code-flow


# this view is used for a single purpose: associating a user with the initial access token and the refresh token

class SpotifyAuthorization(GenericAPIView):
    



class SpotifyUserAuth(CreateAPIView):
    # let's 
    serializer_class = SucReadSerializer

    def post(request, *args, **kwargs):
        # this function is called whenever a new user registers to the application
        # to get the access code

        # create a request to Spotify's authorization server 
        #  1. build the query parameters: according to https://developer.spotify.com/documentation/web-api/tutorials/code-flow
        query_parameters = {"client_id": CLIENT_ID, 
                            "response_type": "code", 
                            "redirect_uri": USER_AUTH_REDIRECT_URI, 
                            # "state":, 
                            "scope": API_SCOPES
                            }

        # 2. send a get request
        spotify_response = rq.get(url='https://accounts.spotify.com/authorize?', # the url is copy pasted from the the spotify developper api documentation 
                               params=query_parameters)

        # using the authentication code
        if not spotify_response.ok:
            # the fields are chosen according to the following link: 
            # https://www.w3schools.com/python/ref_requests_response.asp

            return Response(data={"error_message": "spotify authorization failed", 
                                  "spotify_error": spotify_response.reason}, 
                            status=st.HTTP_500_INTERNAL_SERVER_ERROR)
    
        # at this point, spotify provided an authorization code that can be used to extract an access and refresh token
        code = spotify_response.json()['code']

        # send an authorization from the user
        user_auth_query_params = {
            "code": code,
            "redirect_uri": USER_AUTH_REDIRECT_URI,
            "grant_type": "authorization_code"  
        }

        headers = {
            "Authorization": f"Basic {CLIENT_ID}:{CLIENT_SECRET}",
            'content-type': 'application/x-www-form-urlencoded'
        }

        # send a request
        spotify_user_auth = rq.post(url='https://accounts.spotify.com/api/token', # copy-pasted from the guide
                                    params=user_auth_query_params,
                                    headers=headers
                                    )
        
        if not spotify_response.ok:
            return Response(data={"error_message": "the user did not authorize the application",}, 
                            status=st.HTTP_401_UNAUTHORIZED)

        # at this point, spotify should associate an acccess and refresh token for this user
        access_token, refresh_token = 

                

