from django.urls import path, include
from . import views


urlpatterns = [
    path("login", views.login, name='login_view'),
    path("signup", views.signup, name='signup_view'),
    path("test_token", views.test_token, name='test_token_view'),
]
