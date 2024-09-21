# we will use the requests package to send requests to the spotify authentication server

import requests as rq

from typing import Optional
from django.urls import reverse

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status as st
from rest_framework import permissions as pers

from .app_credentials import OAUTH_USER_AGENT, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPES

from .serializers import YtAuthCodeSerializer, YucReadSerializer, YucUpdateSerializer
from .models import YoutubeAuthCode

# Create your views here.
class YoutubeAppCodeView(CreateAPIView):

    serializer_class = YtAuthCodeSerializer

    def _get_authentication(self, request: Request, *args, **kwargs) -> Optional[YoutubeAuthCode]:    
        """this function will basically query the dataset to determine whether the current app Youtube credentials are associated
        with a authorization code
        Args:
            request (Request): a request object: expected to have 'client_id' and 'client_secret' as query parameters
        Returns:
            Optional[YoutubeAuthCode]: either None of an authorization code
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
        query_set = YoutubeAuthCode.objects.filter(client_id__exact=client_id).filter(client_secret__exact=client_secret)
        print(query_set)

        if query_set.count() == 0:
            print("returning none")
            return None
        
        # there should be only object since the YoutubeAuthCode has the 'unique_together' meta data with ('client_id' and 'client_secret')
        return query_set[0]

    
    def get(self, request: Request, *args, **kwargs) -> Response:
        # first try to fetch an existing Youtube authentication 
        print("YoutubeAppCodeView: the get method !!!")

        auth_code_instance = self._get_authentication(request, *args, **kwargs)

        if auth_code_instance is not None:
            # the passed client id and client secrete are associated 
            # with a authorization code
            return Response(data=YtAuthCodeSerializer(auth_code_instance).data, status=st.HTTP_200_OK)


        print("request an authorization code !!", end='\n')

        # now this is the real deal: connecting to google authorization server
        # build the query parameters


        # 1. build the query parameters according to the 'Step1: set authorization parameters' section 
        # in the following guide: https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps#httprest_1

        query_parameters = {"client_id": CLIENT_ID, # the app id
                            "redirect_uri": REDIRECT_URI, # set it to the main page for now
                            "response_page": "code",
                            "scope":  SCOPES,
                            "access_type": "offline",
                            }
        

        # 2. send a get request
        try:
            yt_response = rq.get(url='https://accounts.google.com/o/oauth2/v2/auth?',  #  copied from "step2: Redirect Google's Oauth server" 
                                params=query_parameters,
                                headers={"User-Agent": OAUTH_USER_AGENT},
                                )

            print(f"received a youtube response !!! with status code : {yt_response.status_code}")
        except Exception as e:
            print("Exception raise somewheree")
            return Response(data={"error_message": "something broke while authorizing with Youtube", "python_error": str(e)}, 
                            status=st.HTTP_500_INTERNAL_SERVER_ERROR)

        if not yt_response.ok:
            print("Youtube_response not ok !!!")
            # the fields are chosen according to the following link: 
            # https://www.w3schools.com/python/ref_requests_response.asp
            return Response(data={"error_message": "Youtube authorization failed",
                                  "Youtube_error": yt_response.reason}, 
                            status=st.HTTP_500_INTERNAL_SERVER_ERROR)

        # using the authentication code
        # at this point, Youtube provided an authorization code that can be used to extract an access and refresh token
        print("converting the Youtube respone to json !!")
        try:
            # print(yt_response.text, end='\n')
            code = yt_response.json()['code']

        except Exception as e:
            return Response(data={"error_message": "error while decoding Youtube_response to json", "error_python": str(e)})
            
        # since the query_params field of the request object in immutable, its need to first be copied
        data = request.query_params.copy() # there is a copy method in the QueryDict object (I checked the source code...)

        data['code'] = code                

        # create a record linking the authorization code to the current set of app credentials 
        res = self.post(request)
        
        print("\n response from Youtube !!!")
        print(res.data,end='\n')

        return Response(data=res.data, status=st.HTTP_200_OK)


    def post(self, request: Request, *args, **kwargs):
        print("print YoutubeAuthCode the post method")
        # this block of code is pretty much copied from the self.create method of the CreateAPIView
        # however with a tiny change: using request.query_params instead of query.data
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=st.HTTP_201_CREATED, headers=headers)


    def get_serializer(self, *args, **kwargs) -> YtAuthCodeSerializer:
        # override the method just to add a type hint an make everything abit more readable...
        return super().get_serializer(*args, **kwargs)


class YoutubeUserTokenView(CreateAPIView):    
    permission_classes = [pers.IsAuthenticated]

    serializer_class = YucReadSerializer

    def post(self, request: Request, *args, **kwargs):
        # send a get request to the code 
        base_url = reverse('youtube_app_code_view') # make sure to set the correct endpoint name

        params_as_dict = {"client_id": CLIENT_ID, 'client_secret': CLIENT_SECRET}
        
        # this is definitely a patched solution and needs to be improved !!!
        final_url = f'http://127.0.0.1:8000/{base_url}'

        res: rq.Response = rq.get(url=final_url, 
               params=params_as_dict,
               # save the client id and client secret for the very initial iteration               
               headers={"content-type": "application/json"},
               )

        if res.status_code >= 400:
            return Response(data={"error_message": res}, status=res.status_code)

        print(f"sent the request to Youtube. Got the following response: {res.status_code, res}")

        # extract the code

        # print(f"The authentication code is: {code}")

        return Response(data={"res": res.json()})

        # send an authorization from the user
        user_auth_query_params = {
            "code": code,
            "redirect_uri": REDIRECT_URI,
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
            return Response(data=YucReadSerializer(obj).data, status=st.HTTP_201_CREATED)

        return Response(data={"error_message": s.error_messages}, status=st.HTTP_500_INTERNAL_SERVER_ERROR)


    def get_serializer(self, *args, **kwargs) -> YucReadSerializer:
        return super().get_serializer(*args, **kwargs)
