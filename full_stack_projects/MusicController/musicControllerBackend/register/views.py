import rest_framework.status as st
import rest_framework.permissions as prs

from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView


from .serializers import UserReadSerializer, UserRegisterSerializer, UserLoginSerializer


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
   

class LoginView(APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = [prs.AllowAny]

    def _redirect(self, request:Request|None, user:User|None = None) -> Response:
        username = request.data.get('username', None)

        if username is None and user is None:
            raise KeyError("something is wrong. Can find neither the 'user' not the 'username'")

        if not username:
            username = user.username

        next_url = reverse('user_detail_view', kwargs={"username": username}) #username is used as a keyword argument in the userDetail view

        return redirect(next_url) 


    def post(self, request: Request, format=None):
        serializer = UserLoginSerializer(data=request.data,
            context={ 'request': request })
        
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return self._redirect(request, user=user)


class LogoutView(APIView):
    def get(self, request: Request, format=None):
        logout(request)
        return Response(data={"message": "logout successfully"}, status=st.HTTP_200_OK)


@api_view(['POST'])
def test_token(request:Request) -> Response:
    return Response({})



