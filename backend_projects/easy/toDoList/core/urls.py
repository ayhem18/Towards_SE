from django.urls import include, path

from . import views 


urlpatterns = [
    # setting the 'name' parameter makes my life much easier afterwards as I can simply use the django.urls.reverse function to find the needed url just by a meaningful human-understandable name
    path("", views.home, name='home_view'), 
    path("home/", views.home, name='home_view'),


    path("account/", views.account_html, name='account_view'),
    path("account_json/", views.account_json, name='account_json_view'),

]



