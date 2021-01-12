import time
import datetime

from django.db import transaction
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from django.core.cache import cache

from django_auth_admin.api_path import API_PATH
from django_auth_admin.base_viewset import BaseViewSet
from django_auth_admin.jwt_authorization import JWTAuthentication, AdminPermission
from users.models import UserBase, Menu, District, Street, Role, Department, Api, City
from users.serializers import ListUserBaseSerializer, UserBaseSerializer, LoginSerializer, MenuSerializer, \
    DistrictSerializer, StreetSerializer, RoleSerializer, DepartmentSerializer, ApiSerializer, \
    ListMenuSerializer, ListRoleSerializer, CitySerializer
from rest_framework_jwt.settings import api_settings

expiration_delta = api_settings.JWT_EXPIRATION_DELTA
refresh_expiration_delta = api_settings.JWT_REFRESH_EXPIRATION_DELTA


def encode_handler(instance, is_refresh=False):
    # 根据用户对象 生成 token 信息
    payload = jwt_payload_handler(instance)
    if is_refresh:
        payload['refresh'] = int(time.mktime((datetime.datetime.now() + refresh_expiration_delta).timetuple()))
    token = jwt_encode_handler(payload)
    return token


class TokenViewSet(BaseViewSet):
    queryset = UserBase.objects.get_queryset().order_by('-id')
    authentication_classes = ()
    permission_classes = ()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'retrieve_person']:
            return ListUserBaseSerializer
        elif self.action == 'login':
            return LoginSerializer
        return UserBaseSerializer

    # 登录
    def login(self, request, *args, **kwargs):
        req_data = request.data
        username = req_data.get('username')
        password = req_data.get('password')
        if not username or not password:
            return Response("参数校验错误")
        instance_list = UserBase.objects.filter(username=req_data['username'])
        if not len(instance_list):
            return Response("登陆失败，用户名不存在")
        instance = instance_list.first()
        if not instance.check_password(password):
            return Response("登陆失败，密码错误")
        if not instance.is_active:
            return Response("账户状态异常，无法登陆，请联系管理员")
        token = encode_handler(instance)
        refresh_token = encode_handler(instance, True)
        return Response({'expire': expiration_delta, 'token': token, 'refresh_token': refresh_token})


class AuthTokenViewSet(TokenViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AdminPermission,)

    # 刷新认证
    def refresh(self, request, *args, **kwargs):
        token = encode_handler(request.user)
        refresh_token = encode_handler(request.user, True)
        payload = request.auth
        # refresh_token 只能被使用一次，使用过后需要添加到 cache 黑名单
        cache.set("auth-black:token:{}".format(payload['refresh_token'].split('.')[2]), 'token',
                  timeout=request.auth['exp'] - int(time.time()) + 5)
        return Response({'expire': expiration_delta, 'token': token, 'refresh_token': refresh_token})

    # 退出登录
    def logout(self, request, *args, **kwargs):
        payload = request.auth
        cache.set("auth-black:token:{}".format(payload['token'].split('.')[2]), 'token',
                  timeout=request.auth['exp'] - int(time.time()) + 5)
        return Response({'msg': '退出成功'})


class UserBaseViewSet(AuthTokenViewSet):
    queryset = UserBase.objects.get_queryset().select_related("department").prefetch_related("role").order_by('id')

    def filter_by_department(self, request):
        req_user = request.user
        # 获取当前用户所拥有的所有的部门的权限信息
        departments = sum([role.departments for role in req_user.role.all()], [])
        if departments:
            # 部门权限信息不为空，根据部门信息进行过滤
            queryset = self.filter_queryset(self.get_queryset().filter(department__in=departments))
        else:
            # 部门权限信息为空，只能查看到自身的数据
            queryset = self.filter_queryset(self.get_queryset().filter(id=req_user.id))
        return queryset

    def list(self, request, *args, **kwargs):
        """
        根据用户所在的部门信息和角色拥有的部门权限信息，对数据进行过滤，
        """
        queryset = self.filter_by_department(request)
        # 结果集分页
        page = self.paginate_queryset(queryset)
        result_data = self.get_serializer(page, many=True).data
        return Response(dict(self.get_paginated_response(result_data), **{'msg': '查询成功'}))

    def create(self, request, *args, **kwargs):
        req_user = request.user
        req_data = request.data.copy()
        # 头像处理
        if req_data.get('head_image'):
            req_data.pop('head_image')
        req_data['create_user'] = req_data['update_user'] = req_user.id  # 创建用户
        req_data['password'] = UserBase.set_password(req_data['password'])
        instance = self.add_instance(req_user, self.get_serializer_class(), req_user)
        return Response({'id': instance.id, 'msg': '新增成功'})

    def update(self, request, *args, **kwargs):
        req_user = request.user
        req_data = request.data.copy()
        if req_data.get('password'):
            req_data['password'] = UserBase.set_password(req_data['password'])
        instance = self.get_object()
        self.update_instance(req_data, self.get_serializer_class(), instance, req_user)
        return Response({'id': instance.id, 'msg': '更新成功'})

    def retrieve_person(self, request, *args, **kwargs):
        instance = request.user
        result_data = self.get_serializer(instance).data
        return Response(dict(result_data, **{'msg': '查询成功'}))

    def destroy(self, request, *args, **kwargs):
        # 删除指定对象，对应删除  role
        instance = self.get_object()
        instance.delete()
        return Response({'msg': '删除成功'})


class MenuViewSet(BaseViewSet):
    queryset = Menu.objects.get_queryset().select_related("parent").order_by('order_num')
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AdminPermission,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ListMenuSerializer
        return MenuSerializer

    def list(self, request, *args, **kwargs):
        # 查询包含分页的结果
        queryset = self.filter_queryset(self.get_queryset())
        return Response({'msg': '查询成功'})

    def create(self, request, *args, **kwargs):
        req_user = request.user
        req_data = request.data.copy()
        with transaction.atomic():
            instance = self.add_instance(req_data, self.get_serializer_class(), request.user)
            # 如果当前新增的类型是  权限，则需要对应操作  api-menu 表
            if req_data['type'] == 2 and request.data.get('perms'):
                Api.objects.values_list("path", "id").filter()
                add_menu_api_list = [MenuApi(**dict(
                    api=api,
                    menu=instance.id,
                    create_user=req_user.id,
                    update_user=req_user.id,
                )) for api in request.data['perms']]
                MenuApi.objects.bulk_create(add_menu_api_list)
            # todo: 新增权限时，需要把对应的权限新增到用户角色体系中
            role_id_list = list(RoleUserBase.objects.values_list("role", flat=True).filter(user_base=req_user.id))
            add_role_menu_list = [RoleMenu(**dict(
                role=role_id,
                menu=instance.id,
                create_user=req_user.id,
                update_user=req_user.id
            )) for role_id in role_id_list]
            RoleMenu.objects.bulk_create(add_role_menu_list)
        return Response({'id': instance.id, 'msg': '新增成功'})

    def destroy(self, request, *args, **kwargs):
        # 删除指定对象，需要级联删除所有的子对象
        instance = self.get_object()
        instance.delete()
        return Response({'msg': '删除成功'})

    def perm_list(self, request, *args, **kwargs):
        # 指定用户的的权限列表，包含页面权限和数据权限
        req_user = request.user
        menus = []
        perms = []
        # 获取当前用户所拥有的所有的角色  ->  所对应的所有权限信息
        role_id_list = list(RoleUserBase.objects.values_list('role', flat=True).filter(user_base=req_user.id))
        menu_id_list = list(set(list(RoleMenu.objects.values_list("menu", flat=True).filter(role__in=role_id_list))))
        # 当前用户拥有页面权限
        if menu_id_list:
            menu_instance_list = Menu.objects.filter(pk__in=menu_id_list)
            # 目录和菜单对象
            menus = ListMenuSerializer(menu_instance_list.all(), many=True).data
            perms = list(
                Api.objects.values_list("path", flat=True).filter(pk__in=list(
                    MenuApi.objects.values_list("api", flat=True).filter(
                        pk__in=list(menu_instance_list.values_list("id", flat=True).filter(type=2)))
                ))
            )
            perms = list(Api.objects.values_list("format_path", flat=True).filter(is_common=0))
        return Response({"data": {'menus': menus, 'perms': perms}, 'msg': '查询成功'})


class RoleViewSet(BaseViewSet):
    queryset = Role.objects.get_queryset().order_by('id')
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AdminPermission,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ListRoleSerializer
        return RoleSerializer

    def create(self, request, *args, **kwargs):
        req_user = request.user
        req_data = request.data.copy()
        with transaction.atomic():
            instance = self.add_instance(req_data, self.get_serializer_class(), request.user)
            if request.data.get('menus'):
                add_role_menu_list = [RoleMenu(**dict(
                    role=instance.id,
                    menu=menu,
                    create_user=req_user.id,
                    update_user=req_user.id,
                )) for menu in request.data['menus']]
                RoleMenu.objects.bulk_create(add_role_menu_list)
        return Response({'id': instance.id, 'msg': '新增成功'})

    def retrieve(self, request, *args, **kwargs):
        # 查询角色详情
        instance = self.get_object()
        result_data = self.get_serializer(instance).data
        result_data['menu_id_list'] = result_data['menu_id_list'].split(',') if result_data['menu_id_list'] else []
        return Response(dict(result_data, **{'msg': '查询成功'}))


class DepartmentViewSet(BaseViewSet):
    queryset = Department.objects.get_queryset().order_by('id')
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AdminPermission,)

    def get_serializer_class(self):
        return DepartmentSerializer


class CityViewSet(BaseViewSet):
    queryset = City.objects.get_queryset().order_by('id')
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AdminPermission,)

    def get_serializer_class(self):
        return CitySerializer


class DistrictViewSet(BaseViewSet):
    queryset = District.objects.get_queryset().order_by('id')
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AdminPermission,)

    def get_serializer_class(self):
        return DistrictSerializer


class StreetViewSet(BaseViewSet):
    queryset = Street.objects.get_queryset().order_by('id')
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AdminPermission,)

    def get_serializer_class(self):
        return StreetSerializer


class ApiViewSet(BaseViewSet):
    queryset = Api.objects.get_queryset().order_by('id')
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AdminPermission,)

    def get_serializer_class(self):
        return ApiSerializer

    def list(self, request, *args, **kwargs):
        req_user = request.user
        api_obj = API_PATH()
        api_list = api_obj.get_apis()
        # 查询当前数据库中的所有的api接口信息
        now_api_list = list(Api.objects.all().values_list("path", flat=True))
        # todo: 两者进行对比，区分出需要 新增的api 和 需要修改的api 和 需要删除的api
        add_api_list = []
        for info in api_list:
            if info['path'] in now_api_list:
                continue
            info['is_common'] = 0
            info['create_user'] = info['update_user'] = req_user.id
            info['format_path'] = info['path'].split('/api/')[1].replace('/', ':')
            if "common" in info['path']:
                info['is_common'] = 1
                info['format_path'] = ""
            add_api_list.append(Api(**info))
        Api.objects.bulk_create(add_api_list)
        return Response({'data': api_list, 'msg': '查询成功'})
