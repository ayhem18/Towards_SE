"""
This script contains Model Serializers based on the Rest Framework
"""

from .models import Blog, Tag

from rest_framework.serializers import ModelSerializer

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class BlogSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
        # the default value of the depth parameter is '1' and that's why only the id of the 'tags' are displayed in the json file
        depth = 2




