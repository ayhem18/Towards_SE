from django.shortcuts import render

# let's get some views out of the way here
from django.http import HttpRequest, HttpResponse, JsonResponse 

# build a class-based view to create a room
from rest_framework import generics, status # using status for better response status
from rest_framework.request import Request # a better Request class that can handle different Request types

from .models import Room
from .serializers import RoomSerializer, CreateRoomSerializer


def main_view(request: Request) -> HttpResponse:
    return HttpResponse(f"this is the main request. recived with query string: {request.data}")



class RoomView(generics.ListAPIView):
    # the idea here is to set the query set
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class CreateRoomView(generics.CreateAPIView):
    serializer_class = CreateRoomSerializer

    def post(self, 
            request: Request, 
            format=None # not sure what this does honestly
            ):
        if not self.request.session.exists(self.request.session.session_key):
            # basically check if the user is connecting from an active session
            self.request.session.create() # 

        ser = self.serializer_class(data=request.data)

        if not ser.is_valid():
            # the data passed by the user is not valid
            return JsonResponse(data={"data": ser.data, "error_message": ser.error_messages},
                                status=status.HTTP_400_BAD_REQUEST)

        guest_can_pause = ser.data.guest_can_pause
        votes_2_skip = ser.data.votes_to_skip
        host = self.request.session.session_key 

        try:
            room = Room.objects.get(host__exact=host)
        except Room.DoesNotExist:
            # this means the user is creating a room for the first time (or at least a room with this very specific session id)
            room = ser.create({"gue"})



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

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
