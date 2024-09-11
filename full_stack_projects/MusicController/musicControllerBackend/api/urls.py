from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.main_view, name='main_view'), # an initial default view 
    path("users/", views.ListUserView.as_view(), name='list_users_view'), # an initial default view 
    path("users/<slug:username>/", views.UserDetail.as_view(), name="user_detail_view"),
    path("rooms/create/", views.CreateRoomView.as_view(), name="room_create_view"),
    # path("rooms/list/", views.CreateRoomView.as_view(), name="room_create_view"),
]
