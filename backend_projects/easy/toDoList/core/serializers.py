from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer

from .models import Group, Task

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        # do not thinkg serializing the password is a good idea
        fields = ['username', 'email', 'first_name', 'last_name']


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        depth = 2
    