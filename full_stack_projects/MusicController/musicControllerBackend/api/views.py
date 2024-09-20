from rest_framework import generics as gn, status as st, permissions as prs 
from rest_framework.request import Request 
from rest_framework.response import Response 

from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.db.models import F

from .models import MusicRoom
from .serializers import MusicRoomWriteSerializer, MusicRoomReadSerializer
from .api_permissions import RoomOwnerPermission
from register.views import UserReadSerializer


def main_view(request: Request) -> HttpResponse:
    return HttpResponse(f"this is the main request. This is the home page !!")


MAX_ROOMS_PER_USERS = 5

# list all users in the platform
class ListUserView(gn.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserReadSerializer
    

# display a user given a detail
class UserDetail(gn.mixins.RetrieveModelMixin,
                    gn.mixins.UpdateModelMixin,
                    gn.mixins.DestroyModelMixin,
                    gn.GenericAPIView):

    # only authenticated users can view user details
    permission_classes = [prs.IsAuthenticated]
    
    queryset = User.objects.all()
    serializer_class = UserReadSerializer
    # use the username to lookup users
    lookup_url_kwarg='username'
    lookup_field='username'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request: Response, *args, **kwargs):
        # extract the username from the request
        # and call the destroy method with the username (extracted from the user request's field.)
        return self.destroy(request, args=[request.user.username]) 


# create a room: the created room will be associated with the request's owner
class CreateRoomView(gn.CreateAPIView):    
    # only authenticated users can create rooms
    permission_classes = [prs.IsAuthenticated]
    
    # use the serializer
    serializer_class = MusicRoomWriteSerializer

    def post(self,
             request: Request):
        _data = request.data.copy()
        _data['host'] = request.user

        ser = self.serializer_class(data=_data, 
                                    context={"username": request.user.username} # passing an extra context for it to be used with default creation_order generation function
                                    )

        if not ser.is_valid():
            # the data passed by the user is not valid
            return JsonResponse(data={"data": ser.data, "error_message": ser.error_messages},
                                status=st.HTTP_400_BAD_REQUEST)
        
        print("is_valid called")
        # at this point, we know the request is valid: extract the values of the fields
        votes2skip = ser.data['votes_to_skip']
        username = ser.data['host']
        room_code = ser.data.get('code') # the code 

        try:
            room = MusicRoom.objects.get(code__exact=room_code) 
            # if the 'get' method does not throw an error, then the room for the code already exists
            ser.update(room, validated_data={"votes_to_skip": votes2skip})

        except MusicRoom.DoesNotExist:
            # this means the room does not exist yet.
            rooms_created_by_user = MusicRoom.objects.filter(host__username=username) # host__exact will match the query with the primary key...
            n = len(rooms_created_by_user)

            # verify if the user has reached the limit of number of rooms created
            if n == MAX_ROOMS_PER_USERS:
                return JsonResponse(data={"data": {"num_rooms_created_by_user": n}, 
                                          "error_message": "You reached your free limit of number of rooms created"}, 
                                    status=st.HTTP_412_PRECONDITION_FAILED)

            # create the room    
            room = ser.create(ser.validated_data)
        
        return JsonResponse(data={"data": MusicRoomReadSerializer(room).data}, 
                            status=st.HTTP_201_CREATED)


# List all the rooms associated with a given user
class ListRoomsByUserView(gn.ListAPIView):
    # the main goal of this view is to list all the rooms created by the user with the given username

    # the queryset will simply the set of rooms
    queryset = MusicRoom.objects.all()
    
    # the serializer will be used to present the data: 
    serializer_class = MusicRoomReadSerializer

    # the slugfield will be the username of the 'host' field in the Room object

    lookup_url_kwarg='username'
    lookup_field='host__username'

    _context = {} # this will contain the username

    def get_queryset(self):
        username = self._context[self.lookup_url_kwarg]
        return self.queryset.filter(**{self.lookup_field:username})

    def get(self, request, *args, **kwargs):
        # the default methdo calls the list method from the ListViewMixin
        # the list method does not call the get_object_method which filters the query set using the lookup_url_kwarg
        # so basically the default implementation returns the 'queryset' field as it is

        # to modify this behavior: override the get_queryset to return users 
        self._context[self.lookup_url_kwarg] = kwargs[self.lookup_url_kwarg]

        return super().get(request, *args, **kwargs)


class RoomDetailUserCreationOrder(gn.mixins.RetrieveModelMixin,
                    gn.mixins.UpdateModelMixin,
                    gn.mixins.DestroyModelMixin,
                    gn.GenericAPIView):

    queryset = MusicRoom.objects.all()

    username_field = 'username'
    username_keyword = 'username'

    creation_order_field = 'creation_order'
    creation_order_keyword = 'creation_order'

    read_room_serializer = MusicRoomReadSerializer
    serializer_class  = MusicRoomReadSerializer

    # creating a room is allowed only for authorized users
    permission_classes = [prs.IsAuthenticated, RoomOwnerPermission]

    def get_permissions(self):
        # the parent get_permissions simply returns the value of the permissions classes
        
        # This view accepts 3 HTTP requests: get, put, delete
        # get should be accessible to any authenticated user
        # put and delete should be accessible only for the creators of those specific rooms

        if self.request.method == 'GET':
            return super().get_permissions()[:1] # return [IsAuthenticated] 

        return super().get_permissions()[1:] # returns [RoomOwnerPermission]

    # override get_object to filter objects both with username and the creation_order subfield
    def get_object(self) -> MusicRoom:
        # this line is copied from the super().get_object method
        queryset = self.filter_queryset(self.get_queryset())

        # extend the filtering to consider both username & creation order 
        filter_kwargs = {f'host__{self.username_field}': self.kwargs[self.username_keyword], self.creation_order_field: self.kwargs[self.creation_order_keyword]}
        
        # this method is tricky because it assumes the query result is at most a single object
        obj = gn.get_object_or_404(queryset, **filter_kwargs)


        self.check_object_permissions(self.request, obj)

        # print(obj)

        return obj

    def get(self, request, *args, **kwargs):
        try:
            return self.retrieve(request, *args, **kwargs)
        except KeyError:
            error_message = f"The view expects the arguments {[self.username_keyword, self.creation_order_keyword]} to be passed in the url"
            return JsonResponse(data={"error_message": error_message}, status=st.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object() # the instance is a MusicRoom record, helps with making the code a tiny bit more readable
        instance_creation_date = instance.created_at
        # destroy the object
        self.perform_destroy(instance)

        # extract all the rooms created by the user after the 'instance_creation_date'
        next_rooms = MusicRoom.objects.filter(host__username=kwargs[self.username_keyword]).filter(created_at__gt=instance_creation_date)


        # the idea here is to decrement the 'creation_order' field of each room created later than the selected instance
        # the explanation of the use of the magical 'F' function can be found here:
        # https://docs.djangoproject.com/en/5.1/ref/models/expressions/#django.db.models.F 
        next_rooms.update(creation_order=F('creation_order') - 1) # "update" automatically saves the new objects to the database (no need for next_rooms.save())

        return Response(status=st.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        try:
            return self.destroy(request, *args, **kwargs)
        except KeyError:
            error_message = f"The view expects the arguments {[self.username_keyword, self.creation_order_keyword]} to be passed in the url"
            return JsonResponse(data={"error_message": error_message}, status=st.HTTP_400_BAD_REQUEST)

    
