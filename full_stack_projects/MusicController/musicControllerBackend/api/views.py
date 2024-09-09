from django.shortcuts import render

# let's get some views out of the way here
from django.http import HttpRequest, HttpResponse, JsonResponse 

# build a class-based view to create a room
from rest_framework import generics, status # using status for better response status
from rest_framework.request import Request # a better Request class that can handle different Request types

from .models import MusicRoom
from .serializers import MusicRoomWriteSerializer, MusicRoomReadSerializer


def main_view(request: Request) -> HttpResponse:
    return HttpResponse(f"this is the main request. recived with query string: {request.data}")


# creating a music room should be allowed only for authenticated users
class RoomView(generics.CreateAPIView):
    serializer_class = MusicRoomWriteSerializer

    def post(self,
             request: Request):
                
        ser = self.serializer_class(data=request.data)

        if not ser.is_valid():
            # the data passed by the user is not valid
            return JsonResponse(data={"data": ser.data, "error_message": ser.error_messages},
                                status=status.HTTP_400_BAD_REQUEST)
        
        votes2skip = ser.data.votes_to_skip
        host = self.request.session.session_key 

        try:
            room = MusicRoom.objects.get(host__exact=host)
        except MusicRoom.DoesNotExist:
            # this means the user is creating a room for the first time (or at least a room with this very specific session id)
            room = ser.create()



from django.contrib.auth.models import User
from register.views import UserReadSerializer

class ListUserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserReadSerializer
    

class UserDetail(generics.mixins.RetrieveModelMixin,
                    generics.mixins.UpdateModelMixin,
                    generics.mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserReadSerializer
    # use the username to lookup users
    lookup_url_kwarg='username'
    lookup_field='username'

