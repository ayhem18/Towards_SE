# we will use the requests package to send requests to the spotify authentication server

import requests as rq

from typing import Optional
from django.urls import reverse

from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status as st
from rest_framework import permissions as pers

from .credentials import CLIENT_ID, API_SCOPES, USER_AUTH_REDIRECT_URI, CLIENT_SECRET    
from .serializers import SucReadSerializer, SucUpdateSerializer, SpotifyAuthCodeSerializer
from .models import SpotifyAuthCode

# since we will use the authorization of the user once...
# then the authorization code flow is the most suitable: 
# https://developer.spotify.com/documentation/web-api/tutorials/code-flow


# this view is used for a single purpose: associating a user with the initial access token and the refresh token
class SpotifyAuthCodeView(CreateAPIView, RetrieveAPIView):

    serializer_class = SpotifyAuthCodeSerializer

    def _get_authentication(self, request: Request, *args, **kwargs) -> Optional[SpotifyAuthCode]:    
        # extract the authorization code
        client_id = request.query_params.get('client_id', None)        
        client_secret = request.query_params.get('client_secret', None)        

        if client_id is None or client_secret is None:
            return Response(data={
                                "error_message": 
                                f"Both client id and client secret must be passed: {client_id}, {client_secret}"  
                                }, status=st.HTTP_400_BAD_REQUEST
                            )
        query_set = SpotifyAuthCode.objects.filter(client_id__exact=client_id).filter(client_secret__=client_secret)

        if query_set.count == 0:
            return None
        
        # there should be only object
        return query_set[0]

    
    def get(self, request: Request, *args, **kwargs):
        # first try to fetch an existing spotify authentication 
        auth_code_instance = self._get_authentication(request, *args, **kwargs)

        if auth_code_instance is not None:
            # the passed client id and client secrete are associated 
            # with a authorization code
            return Response(data=SpotifyAuthCodeSerializer(auth_code_instance).data, status=st.HTTP_200_OK)


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
        
        # add the code to the request query parameters
        request.query_params['code'] = code

        # create a record linking the authorization code to current set of credentials
        res = self.post(request)

        return Response(data=res.data, status=st.HTTP_200_OK)


    def post(self, request: Request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SpotifyUserAuth(CreateAPIView):
    # let's 
    permission_classes = [pers.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # send a get request to the 
        res = rq.get(url=reverse(), 
               params={"client_id": CLIENT_ID, 'client_secret': CLIENT_SECRET},
               headers={"content-type": "application/json"},
               )

        if not res.ok:
            return Response(data={"error_message": res.reason}, status=res.status_code)
        
        # extract the code
        code = res.json()['code']

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
        
        if not spotify_user_auth.ok:
            return Response(data={"error_message": "the user did not authorize the application",}, 
                            status=st.HTTP_401_UNAUTHORIZED)
        
        spotify_user_auth = spotify_user_auth.json()
        # at this point, spotify should associate an acccess and refresh token for this user
        access_token, refresh_token, expires_in = spotify_user_auth['access_token'], spotify_user_auth['refresh_token'], spotify_user_auth['expires_in'] 

        # save the tokens with the user
        s = SucReadSerializer(data={"access_token": access_token, 
                                    "refresh_token": refresh_token, 
                                    "user": request.user})
        
        if s.is_valid():
            obj = s.create(s.validated_data)
            s.save()
            return Response(data=SucReadSerializer(obj).data, status=st.HTTP_201_CREATED)

        return Response(data={"error_message": s.error_messages}, status=st.HTTP_500_INTERNAL_SERVER_ERROR)
