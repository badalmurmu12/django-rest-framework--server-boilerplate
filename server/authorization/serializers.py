from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework import serializers


import random

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        newuser = User.objects.create(mobile=validated_data['mobile'])
        return newuser

    def _create(self, validated_data):
        newuser = User.objects._create_user(mobile=validated_data['mobile'], password=validated_data['password'])
        return newuser

    def userexitornot(self, validated_data):
        guestuser = User.objects.get(validated_data['mobile'])
        return guestuser

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile', 'first_name', 'last_name']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
