from django.urls import path

from . import views


urlpatterns = [
                path("page", views.index, name='index'), 
                path("home", views.say_hello, name='helloView'), 
                path("html", views.load_html, name='html_loader'), 
                path("", views.anotherView, name='anotherView')
            ]
