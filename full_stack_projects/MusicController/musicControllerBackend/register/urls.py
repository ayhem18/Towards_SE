from django.urls import path
from . import views


urlpatterns = [
    path("signup/", views.SignUpUserView.as_view(), name='signup_view'),
    # path('signup/', views.signup, name='signup_view'), 
    path("login/", views.login, name='login_view'),
    path("test_token/", views.test_token, name='test_token_view'),
]
