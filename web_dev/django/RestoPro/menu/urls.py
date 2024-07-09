from django.urls import path, re_path # re_path allows to create path using regular expressions

from . import views

urlpatterns = [
                path("dishes", views.display_dishes, name='dishes'),
                path("page", views.index, name='index'), 
                # basically path("path/<param>") will pass the value of param as an extra argument to the view function...
                # path("getuser/<name>/<id>", views.get_user, name='get_user_view'), # an exmaple of an url that matches this patter: getuser/ayhem/23
                path("getuser/", views.get_user2, name='get_user_view2'), # getuser/?name=name_value&id=id_value; those are processed through the HTTP methods 
            ]
