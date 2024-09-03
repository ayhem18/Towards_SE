from .models import Room

from rest_framework.serializers import ModelSerializer

class BlogSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        # the default value of the depth parameter is '1' and that's why only the id of the 'tags' are displayed in the json file
        depth = 1
