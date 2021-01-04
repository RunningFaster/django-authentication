from rest_framework import serializers
from users.models import UserBase, Menu, District, Street, Committee


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)


class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBase
        exclude = ['is_active']


class ListUserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBase
        exclude = ['password']


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class StreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Street
        fields = '__all__'


class CommitteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Committee
        fields = '__all__'
