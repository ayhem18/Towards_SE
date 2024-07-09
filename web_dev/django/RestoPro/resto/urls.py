from django.urls import path # re_path allows to create path using regular expressions

from . import views

urlpatterns = [
    path("about", views.about_view, name='about'), 
]

