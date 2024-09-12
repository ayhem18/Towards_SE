from rest_framework import generics as gn, status as st, permissions as prs 
from rest_framework.request import Request 

from django.contrib.auth.models import User

from django.http import HttpResponse, JsonResponse
from .models import MusicRoom
from .serializers import MusicRoomWriteSerializer, MusicRoomReadSerializer

from register.views import UserReadSerializer


def main_view(request: Request) -> HttpResponse:
    return HttpResponse(f"this is the main request. recived with query string: {request.data}")


MAX_ROOMS_PER_USERS = 3


class CreateRoomView(gn.CreateAPIView):    
    # only authenticated users can create rooms
    permission_classes = [prs.IsAuthenticated]
    
    # use the serializer
    serializer_class = MusicRoomWriteSerializer

    def post(self,
             request: Request):
        _data = request.data.copy()
        _data['host'] = request.user

        ser = self.serializer_class(data=_data)

        if not ser.is_valid():
            # the data passed by the user is not valid
            return JsonResponse(data={"data": ser.data, "error_message": ser.error_messages},
                                status=st.HTTP_400_BAD_REQUEST)

        # at this point, we know the request is valid: extract the values of the fields
        votes2skip = ser.data['votes_to_skip']
        username = ser.data['host']
        room_code = ser.data.get('code') # the code 

        print(username, votes2skip, room_code)

        try:
            room = MusicRoom.objects.get(code__exact=room_code) 
            # if the 'get' method does not throw an error, then the room for the code already exists
            ser.update(room, validated_data={"votes_to_skip": votes2skip})

        except MusicRoom.DoesNotExist:
            # this means the room does not exist yet. 
            # verify if the user has created enough

            rooms_created_by_user = MusicRoom.objects.filter(host__username=username) # host__exact will match the query with the primary key...
            n = len(rooms_created_by_user)
        
            if n == MAX_ROOMS_PER_USERS:
                return JsonResponse(data={"data": {"num_rooms_created_by_user": n}, "error_message": "You reached your free limit of number of rooms created"}, 
                                    status=st.HTTP_412_PRECONDITION_FAILED)

            # create the room    
            room = ser.create(ser.validated_data)
        
        return JsonResponse(data={"data": MusicRoomReadSerializer(room).data}, status=st.HTTP_201_CREATED)


class ListUserView(gn.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserReadSerializer
    

class UserDetail(gn.mixins.RetrieveModelMixin,
                    gn.mixins.UpdateModelMixin,
                    gn.mixins.DestroyModelMixin,
                    gn.GenericAPIView):

    # only authenticated users can be view user details
    permission_classes = [prs.IsAuthenticated]
    
    queryset = User.objects.all()
    serializer_class = UserReadSerializer
    # use the username to lookup users
    lookup_url_kwarg='username'
    lookup_field='username'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
