from rest_framework import serializers
from users.models import UserBase


class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBase
        fields = '__all__'


class ListUserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBase
        exclude = ['password']
