from rest_framework import serializers
from users.models import UserBase, Menu, District, Street, Committee, Role


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)


class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBase
        exclude = ['is_active']


class ListUserBaseSerializer(serializers.ModelSerializer):
    sex_desc = serializers.CharField(source="get_sex_display")
    is_active_desc = serializers.CharField(source="get_is_active_display")
    role_id_list_desc = serializers.SerializerMethodField()

    class Meta:
        model = UserBase
        exclude = ['password']

    def get_role_id_list_desc(self, obj):
        if not obj.role_id_list:
            return ''
        name_list = ",".join(
            list(Menu.objects.values_list("name", flat=True).filter(pk__in=obj.role_id_list.split(','))))
        return name_list


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
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
