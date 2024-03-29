from rest_framework import serializers
from organization.models import UserBase, Menu, Role, Department, Api


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)


class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBase
        exclude = ['is_active']


class ApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Api
        fields = '__all__'


class ListUserBaseSerializer(serializers.ModelSerializer):
    sex_desc = serializers.CharField(source="get_sex_display")
    is_active_desc = serializers.CharField(source="get_is_active_display")

    role_name = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()

    class Meta:
        model = UserBase
        exclude = ['password']

    def get_role_name(self, obj):
        role_instance = obj.role.all()
        return ",".join([i.name for i in role_instance])

    def get_department_name(self, obj):
        if obj.department:
            return obj.department.name
        return ""


class MenuSerializer(serializers.ModelSerializer):
    api = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Menu
        fields = '__all__'


class PermmenuMenuSerializer(serializers.ModelSerializer):
    perms = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        exclude = ('api',)

    def get_perms(self, obj):
        apis = getattr(obj, "apis", obj.api.all())
        return ",".join([api.format_path for api in apis if api.format_path])


class ListMenuSerializer(serializers.ModelSerializer):
    api = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = '__all__'

    def get_api(self, obj):
        apis = getattr(obj, "apis", obj.api)
        return [api.id for api in apis.all()]


class ListRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    menus = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Role
        fields = '__all__'

    def validate(self, attrs):
        # 校验menus信息是否符合规范
        if attrs.get('menus') is not None:
            if Api.objects.filter(pk__in=attrs['menus']).count() != len(attrs['menus']):
                raise serializers.ValidationError("权限信息有误，请核实")
            del attrs["menus"]
        return attrs


class DepartmentSerializer(serializers.ModelSerializer):
    parent_name = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = '__all__'

    def get_parent_name(self, obj):
        if obj.parent_id:
            return Department.objects.get(pk=obj.parent_id).name
        return ""
