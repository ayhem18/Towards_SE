from django.urls import path
from . import views


urlpatterns = [
    path("signup/", views.SignUpUserView.as_view(), name='signup_view'),
    # path('signup/', views.signup, name='signup_view'), 
    path("login/", views.LoginView.as_view(), name='login_view'),
    path("logout/", views.LogoutView.as_view(), name='logout_view'),
    path("test_token/", views.test_token, name='test_token_view'),    
]
