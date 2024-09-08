import rest_framework.status as st
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from .serializers import UserReadSerializer, UserRegisterSerializer
from django.contrib.auth.models import User


from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.parsers import JSONParser

class SignUpUserView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    # queryset = User.objects.all()

    def get_serializer(self, *args, **kwargs) -> UserRegisterSerializer:
        return super().get_serializer(*args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        print("receiving the post request")
        ser = self.get_serializer(data=request.data)

        if ser.is_valid():
            new_user = ser.create(ser.data)

            new_user_token = Token.objects.create(user=new_user)
            return Response(data={"token": new_user_token.key, "user": UserReadSerializer(new_user).data}, 
                            status=st.HTTP_201_CREATED)

        return Response(data={"error_message": ser.errors}, status=st.HTTP_400_BAD_REQUEST)


    def get(self, request: Request):
        print(request.data)
        return Response({"data": request.data})


@api_view(['POST'])
def login(request:Request) -> Response:
    return Response({})


# @api_view(['POST'])
# def signup(request:Request) -> Response:
#     # let's create a user 
#     ser = UserRegisterSerializer(data=request.data)
#     # data = JSONParser().parse(request)
#     # ser = UserRegisterSerializer(data=data)

#     if ser.is_valid():
#         # save a user instance in the database
#         ser.save()

#         # fetch the user to encrypt the password
#         new_user = User.objects.get(username=request.data.get('username'))
#         new_user.set_password(raw_password=request.data.get('password'))

#         # according to https://www.django-rest-framework.org/api-guide/authentication/#how-authentication-is-determined
#         # this should somehow associate the user with the credentials, no ?
#         new_user_token = Token.objects.create(user=new_user)

#         return Response(data={"token": new_user_token.key, "user": UserReadSerializer(new_user).data})

#     return Response(data={"error_message": ser.errors}, status=st.HTTP_400_BAD_REQUEST)



# @api_view(['POST'])
# def signup(request: Request) -> Response:
#     return Response({"data": "This is the sign up api endpoint"})

@api_view(['POST'])
def test_token(request:Request) -> Response:
    return Response({})

