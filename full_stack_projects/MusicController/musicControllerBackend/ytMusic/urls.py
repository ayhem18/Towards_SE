from django.urls import path

from . import views


urlpatterns = [
    path("_youtube_app_code/", views.YoutubeAppCodeView.as_view(), name='youtube_app_code_view'),  
    path("_youtube_user_token/", views.YoutubeUserTokenView.as_view(), name='youtube_user_token_view'),
]
