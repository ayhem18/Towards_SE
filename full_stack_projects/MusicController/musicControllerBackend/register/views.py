import rest_framework.status as st
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from .serializers import UserReadSerializer, UserRegisterSerializer
from rest_framework.generics import CreateAPIView
from django.contrib.auth import authenticate

class SignUpUserView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    # rewrote the get_serializer as it +  adding the return Type to make things easier...
    def get_serializer(self, *args, **kwargs) -> UserRegisterSerializer:
        return super().get_serializer(*args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)

        if ser.is_valid():
            new_user = ser.create(ser.data)

            new_user_token = Token.objects.create(user=new_user)
            return Response(data={"token": new_user_token.key, "user": UserReadSerializer(new_user).data}, 
                            status=st.HTTP_201_CREATED)

        return Response(data={"error_message": ser.errors}, status=st.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request: Request):
    # get username and pasword
    data = request.data

    username = data.get('username', None)
    password = data.get('password', None)

    print(username, password, sep="~~")

    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)

            return Response(data={"message": "user logged in"}, status=st.HTTP_200_OK)
        else:
            return Response(data={"message": "user not active"}, status=st.HTTP_404_NOT_FOUND)
    else:
        return Response(data={"message": "uncorrect credentials"}, status=st.HTTP_404_NOT_FOUND)    


@api_view(['POST'])
def test_token(request:Request) -> Response:
    return Response({})

