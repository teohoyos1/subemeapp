from pyexpat import model
from rest_framework import serializers
from .models import Fi_file,Fi_file_type

class Fi_file_serializer(serializers.ModelSerializer):
    class Meta:
        model = Fi_file
        fields = ('id','fileType','fileTypeName','fileDescription','files','modified_date')


class Fi_file_type_serializer(serializers.ModelSerializer):
    class Meta:
        model = Fi_file_type
        fields = ('id','name','isActive')