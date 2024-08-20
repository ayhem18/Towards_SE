from django.urls import include, path

from . import views 


urlpatterns = [
    # path("login/", views.login, name='login_view'),
    path('login/', views.MyLoginView.as_view()),
    # path("authenticate/", views.authenticate_user, name='authenticate_user_view'),
    path('register/', views.register_user, name='register_user_view')
]



