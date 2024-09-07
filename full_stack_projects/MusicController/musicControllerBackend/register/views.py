import rest_framework.status as st
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer
from django.contrib.auth.models import User

# Create your views here.

@api_view(['POST'])
def login(request:Request) -> Response:
    return Response({})


@api_view(['POST'])
def signup(request:Request) -> Response:
    # let's create a user 
    ser = UserSerializer(request.data)

    if ser.is_valid():
        # this will create a user instance in the database
        ser.save()
        # fetch the user to encrypt the password
        new_user = User.objects.get(username=request.data.get('username'))
        new_user.set_password(raw_password=request.data.get('password'))

        # according to https://www.django-rest-framework.org/api-guide/authentication/#how-authentication-is-determined
        # this should somehow associate the user with the credentials, no ?
        new_user_token = Token.objects.create(user=new_user)

        return Response(data={"token": new_user_token.key, "user": UserSerializer(new_user).data})

    return Response(data={"error_message": ser.error_messages}, status=st.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def test_token(request:Request) -> Response:
    return Response({})

