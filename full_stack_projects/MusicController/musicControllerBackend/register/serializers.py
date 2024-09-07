from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User


# my code is mostly based on this great tutorial: 
# https://www.codersarts.com/post/how-to-create-register-and-login-api-using-django-rest-framework-and-token-authentication


# this serialize will be used to serializer an existing user
class UserReadSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password', ]
