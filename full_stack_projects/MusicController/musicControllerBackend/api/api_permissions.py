"""
This script contains the definition of custom Permissions
"""
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from .models import MusicRoom

class RoomOwnerPermission(IsAuthenticated):
    def has_permission(self, request, view):
        # basically only authenticated users can access this view
        return super().has_permission(request, view)
    
    def has_object_permission(self, 
                              request: Request, 
                              view, 
                              obj: MusicRoom):
        # the has_object_permission is a bit tricky
        return request.user.username == obj.host.username        
