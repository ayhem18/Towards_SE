from django.contrib.auth.models import User

from rest_framework.serializers import PrimaryKeyRelatedField, StringRelatedField
from rest_framework.serializers import ModelSerializer

from .models import Group, Task

class GroupSerializer(ModelSerializer):
    # as of my understanding of the serializers documentation: 
    # using the PrimaryKeyRelatedField will serializer the owner with only its id
    owner = StringRelatedField(many=False, read_only=True)
    # PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Group
        fields = '__all__'
        depth = 1
    

class TaskSerializer(ModelSerializer):
    group = PrimaryKeyRelatedField(many=False, read_only=True)
    
    class Meta:
        model = Task
        fields = '__all__'
        depth = 1
