# we will use the requests package to send requests to the spotify authentication server

from django.http import QueryDict
from django.http import HttpResponseRedirect

import requests as rq

from typing import Optional
from django.urls import reverse
from django.shortcuts import redirect

from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status as st
from rest_framework import permissions as pers

from .credentials import CLIENT_ID, API_SCOPES, USER_AUTH_REDIRECT_URI, CLIENT_SECRET    
from .serializers import SucReadSerializer, SpotifyAuthCodeSerializer
from .models import SpotifyAuthCode

# since we will use the authorization of the user once...
# then the authorization code flow is the most suitable: 
# https://developer.spotify.com/documentation/web-api/tutorials/code-flow


# this view serves a single purpose: getting a authorization code that
# can be exchanged with an access token
class SpotifyAppCodeView(CreateAPIView):

    serializer_class = SpotifyAuthCodeSerializer

    def _get_authentication(self, request: Request, *args, **kwargs) -> Optional[SpotifyAuthCode]:    
        """this function will basically query the dataset to determine whether the current app spotify credentials are associated
        with a authorization code
        Args:
            request (Request): a request object: expected to have 'client_id' and 'client_secret' as query parameters
        Returns:
            Optional[SpotifyAuthCode]: either None of an authorization code
        """
        print("Trying to get the authentication ")
        # extract the authorization code
        client_id = request.query_params.get('client_id', None)        
        client_secret = request.query_params.get('client_secret', None)        

        if client_id is None or client_secret is None:
            return Response(data={
                                "error_message": 
                                f"Both client id and client secret must be passed: {client_id}, {client_secret}"  
                                }, 
                                status=st.HTTP_400_BAD_REQUEST
                            )
        query_set = SpotifyAuthCode.objects.filter(client_id__exact=client_id).filter(client_secret__exact=client_secret)
        print(query_set)

        if query_set.count() == 0:
            print("returning none")
            return None
        
        # there should be only object since the SpotifyAuthCode has the 'unique_together' meta data with ('client_id' and 'client_secret')
        return query_set[0]

    
    def get(self, request: Request, *args, **kwargs) -> Response:
        # first try to fetch an existing spotify authentication 
        print("SpotifyAppCodeView: the get method !!!")

        auth_code_instance = self._get_authentication(request, *args, **kwargs)

        if auth_code_instance is not None:
            # the passed client id and client secrete are associated 
            # with a authorization code
            return Response(data=SpotifyAuthCodeSerializer(auth_code_instance).data, status=st.HTTP_200_OK)


        print("request an authorization code !!", end='\n')


        # create a request to Spotify's authorization server 
        #  1. build the query parameters: according to https://developer.spotify.com/documentation/web-api/tutorials/code-flow
        query_parameters = {"client_id": CLIENT_ID, 
                            "response_type": "code", 
                            "redirect_uri": USER_AUTH_REDIRECT_URI, 
                            # "state":, 
                            "scope": API_SCOPES
                            }

        # 2. send a get request
        try:
            spotify_response = rq.get(url='https://accounts.spotify.com/authorize?', # the url is copy pasted from the the spotify developper api documentation 
                                params=query_parameters,
                                headers={"content-type": "application/json"}, # send the request as jsonn                                
                                )

            print(f"received spotify response !!! with status code : {spotify_response.status_code}")
        except:
            return Response(data={"error_message": "something broke while authorizing with spotify"}, 
                            status=st.HTTP_500_INTERNAL_SERVER_ERROR)

        if not spotify_response.ok:
            # the fields are chosen according to the following link: 
            # https://www.w3schools.com/python/ref_requests_response.asp
            return Response(data={"error_message": "spotify authorization failed"},
                                #   "spotify_error": spotify_response.reason}, 
                            status=st.HTTP_500_INTERNAL_SERVER_ERROR)
    
        # using the authentication code
        # at this point, spotify provided an authorization code that can be used to extract an access and refresh token
        code = spotify_response.json()['code']
        
        # add the code to the request query parameters
        request.query_params['code'] = code

        # create a record linking the authorization code to the current set of app credentials 
        res = self.post(request)
        
        print("\n response from spotify !!!")
        print(res.data,end='\n')

        return Response(data=res.data, status=st.HTTP_200_OK)


    def post(self, request: Request, *args, **kwargs):
        print("print SpotifyAuthCode the post method")
        # this block of code is pretty much copied from the self.create method of the CreateAPIView
        # however with a tiny change: using request.query_params instead of query.data
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=st.HTTP_201_CREATED, headers=headers)


    def get_serializer(self, *args, **kwargs) -> SpotifyAuthCodeSerializer:
        # override the method just to add a type hint an make everything abit more readable...
        return super().get_serializer(*args, **kwargs)


class SpotifyUserTokenView(CreateAPIView):    
    permission_classes = [pers.IsAuthenticated]

    serializer_class = SucReadSerializer

    def post(self, request: Request, *args, **kwargs):
        # send a get request to the code 
        base_url = reverse('spotify_app_code_view')
        params_as_dict = {"client_id": CLIENT_ID, 'client_secret': CLIENT_SECRET}
        
        # build the url using the request library
        # final_url = rq.Request('GET', 
        #            base_url, 
        #            params={"client_id": CLIENT_ID, 'client_secret': CLIENT_SECRET},).prepare().url

        # temp_query_dict = QueryDict(request.query_params.urlencode(), 
        #                             mutable=True)
        # temp_query_dict.clear()
        # temp_query_dict.update(params_as_dict)
        # final_url = f'http://127.0.0.1:8000/{base_url}?{temp_query_dict.urlencode()}'
        final_url = f'http://127.0.0.1:8000/{base_url}'
    

        # url = Request('GET', 'https://accounts.spotify.com/authorize', params={
        #     'scope': scopes,
        #     'response_type': 'code',
        #     'redirect_uri': REDIRECT_URI,
        #     'client_id': CLIENT_ID
        # }).prepare().url


        res: Response = rq.get(url=final_url, 
               params=params_as_dict,
               # save the client id and client secret for the very initial iteration               
               headers={"content-type": "application/json"},
               )

        if res.status_code >= 400:
            return Response(data={"error_message": res}, status=res.status_code)

        print(f"sent the request to Spotify. Got the following response: {res.status_code, res}")

        # extract the code
        code = res.data['code']

        print(f"The authentication code is: {code}")

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
        
        print("reached the user authorization part !!")

        if not spotify_user_auth.ok:
            return Response(data={"error_message": "the user did not authorize the application",}, 
                            status=st.HTTP_401_UNAUTHORIZED)
        
        spotify_user_auth = spotify_user_auth.json()
        # at this point, spotify should associate an acccess and refresh token for this user
        access_token, refresh_token, expires_in = spotify_user_auth['access_token'], spotify_user_auth['refresh_token'], spotify_user_auth['expires_in'] 

        # save the tokens with the user
        s = self.get_serializer(data={"access_token": access_token, 
                                    "refresh_token": refresh_token, 
                                    "user": request.user})
    
        if s.is_valid():
            obj = s.create(s.validated_data)
            s.save()
            return Response(data=SucReadSerializer(obj).data, status=st.HTTP_201_CREATED)

        return Response(data={"error_message": s.error_messages}, status=st.HTTP_500_INTERNAL_SERVER_ERROR)


    def get_serializer(self, *args, **kwargs) -> SucReadSerializer:
        return super().get_serializer(*args, **kwargs)
