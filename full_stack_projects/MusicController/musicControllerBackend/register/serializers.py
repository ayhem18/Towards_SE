from typing import Dict

from rest_framework import serializers as sers

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

# my code is mostly based on this great tutorial: 
# https://www.codersarts.com/post/how-to-create-register-and-login-api-using-django-rest-framework-and-token-authentication

# this serialize will be used to serialize an existing user
class UserReadSerializer(sers.ModelSerializer):
    class Meta:
        model = User
        # choose the field to return in Json Response
        fields = ['email', 'username', 'first_name', 'last_name']

# serializer to create a new user
class UserRegisterSerializer(sers.ModelSerializer):
    password = sers.CharField(required=True, validators=[validate_password])
    password2 = sers.CharField(required=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields = ('password', 'password2', 'username', 'first_name', 'last_name', 'email')

    # override the validate method to make sure both passwords match
    def validate(self, attrs: Dict):
        print(f"validating: {attrs}")
        if attrs['password'] != attrs['password2']:
            raise sers.ValidationError({"password": "the two passwords do not match"})
        
        a = attrs.copy()
        a.pop('password2')
        # validate the rest of the fields
        super().validate(a)        
        return attrs
    
    def create(self, validated_data: Dict):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
            )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(sers.Serializer):
    username = sers.CharField(write_only=True)

    password = sers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs: Dict):
        username = attrs.get('username')
        pwd = attrs.get('password')

        if username is not None and pwd is not None:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=pwd)
            
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise sers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise sers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
    