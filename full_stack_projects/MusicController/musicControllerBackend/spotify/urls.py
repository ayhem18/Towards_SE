from django.urls import path

from . import views


urlpatterns = [
    path("_spotify_app_code/", views.SpotifyAppCodeView.as_view(), name='spotify_app_code_view'),
    path("_spotify_user_token/", views.SpotifyUserTokenView.as_view(), name='spotify_user_token_view'),
]
