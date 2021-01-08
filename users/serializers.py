from rest_framework import serializers
from users.models import UserBase, Menu, District, Street, Committee, Role, Department, Api, RoleUserBase, Event


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)


class UserBaseSerializer(serializers.ModelSerializer):
    roles = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = UserBase
        exclude = ['is_active']

    def validate(self, attrs):
        # 校验roles信息是否符合规范
        if attrs.get('roles') is not None:
            if Role.objects.filter(pk__in=attrs['roles']).count() != len(attrs['roles']):
                raise serializers.ValidationError("角色信息有误，请核实")
            del attrs["roles"]
        # 校验department_id信息是否符合规范
        if attrs.get('department') is not None:
            if not Department.objects.filter(pk=attrs['department']).count():
                raise serializers.ValidationError("部门信息有误，请核实")
        return attrs


class ApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Api
        fields = '__all__'


class ListUserBaseSerializer(serializers.ModelSerializer):
    sex_desc = serializers.CharField(source="get_sex_display")
    is_active_desc = serializers.CharField(source="get_is_active_display")

    # role_name = serializers.SerializerMethodField()
    # department_name = serializers.SerializerMethodField()

    class Meta:
        model = UserBase
        exclude = ['password']

    def get_role_name(self, obj):
        role_user_base_list = list(RoleUserBase.objects.values_list("role", flat=True).filter(user_base=obj.id))
        name_list = ",".join(Role.objects.values_list('name', flat=True).filter(pk__in=role_user_base_list))
        return name_list

    def get_department_name(self, obj):
        if obj.department:
            return Department.objects.get(pk=obj.department).name
        return ""


class MenuSerializer(serializers.ModelSerializer):
    apis = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Menu
        fields = '__all__'

    def validate(self, attrs):
        # 校验apis信息是否符合规范
        if attrs.get('apis') is not None:
            if Api.objects.filter(pk__in=attrs['apis']).count() != len(attrs['apis']):
                raise serializers.ValidationError("权限信息有误，请核实")
            del attrs["apis"]
        return attrs


class ListMenuSerializer(serializers.ModelSerializer):
    parent_name = serializers.SerializerMethodField()
    parent_id = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = '__all__'

    def get_parent_name(self, obj):
        if obj.parent_id:
            return Menu.objects.get(pk=obj.parent_id).name
        return ""

    def get_parent_id(self, obj):
        if obj.parent_id == 0:
            return None
        return obj.parent_id


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


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
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
