from django.urls import include, path

from . import views 


urlpatterns = [
    path("home/", views.home, name='home'),
    path("login/", views.login, name='login'),
]