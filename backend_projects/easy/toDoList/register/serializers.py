from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        
        # since the django original User model contains numerous fields, I need to specify the fields to be serialized
        fields = ['username', 'email', 'first_name', 'last_name']
        # exclude = ['password']
