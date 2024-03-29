import time
import datetime

from django.db import transaction
from django.db.models import Prefetch
from django.views.decorators.cache import cache_page
from rest_framework.exceptions import *
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from django.core.cache import cache

from basic.api_path import API_PATH
from basic.base_viewset import BaseViewSet
from organization.models import UserBase, Menu, Role, Department, Api
from organization.serializers import ListUserBaseSerializer, UserBaseSerializer, LoginSerializer, MenuSerializer, \
    RoleSerializer, DepartmentSerializer, ApiSerializer, ListMenuSerializer, ListRoleSerializer, PermmenuMenuSerializer
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
        return LoginSerializer

    # 登录
    def login(self, request, *args, **kwargs):
        req_data = request.data
        username = req_data.get('username')
        password = req_data.get('password')
        if not username or not password:
            raise ValidationError("参数校验错误")
        instance_list = UserBase.objects.filter(username=req_data['username'])
        if not len(instance_list):
            raise AuthenticationFailed("登陆失败，用户名不存在")
        instance = instance_list.first()
        if not instance.check_password(password):
            raise AuthenticationFailed("登陆失败，密码错误")
        if not instance.is_active:
            raise AuthenticationFailed("账户状态异常，无法登陆，请联系管理员")
        token = encode_handler(instance)
        refresh_token = encode_handler(instance, True)
        return Response(
            {"data": {'expire': expiration_delta, 'token': token, 'refresh_token': refresh_token}, "msg": "登录成功",
             "status": 1})


class AuthTokenViewSet(TokenViewSet):

    # 刷新认证
    def refresh(self, request, *args, **kwargs):
        token = encode_handler(request.user)
        refresh_token = encode_handler(request.user, True)
        payload = request.auth
        # refresh_token 只能被使用一次，使用过后需要添加到 cache 黑名单
        cache.set("auth-black:token:{}".format(payload['refresh_token'].split('.')[2]), 'token',
                  timeout=request.auth['exp'] - int(time.time()) + 5)
        return Response(
            {"data": {'expire': expiration_delta, 'token': token, 'refresh_token': refresh_token}, "msg": "刷新成功",
             "status": 1})

    # 退出登录
    def logout(self, request, *args, **kwargs):
        payload = request.auth
        cache.set("auth-black:token:{}".format(payload['token'].split('.')[2]), 'token',
                  timeout=request.auth['exp'] - int(time.time()) + 5)
        return Response({"msg": "退出成功", "status": 1})


class UserBaseViewSet(BaseViewSet):
    """
    list: 根据用户所在的部门信息和角色拥有的部门权限信息，对数据进行过滤，只能查询到自己部门下的用户列表
    """
    queryset = UserBase.objects.get_queryset().select_related("department").prefetch_related("role")

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'retrieve_person']:
            return ListUserBaseSerializer
        return UserBaseSerializer

    def get_permissions_queryset(self, request):
        user = request.user
        # 获取当前用户所拥有的所有的部门的权限信息
        permission_department_list = user.get_permission_department_list()
        if permission_department_list:
            # 部门权限信息不为空，根据部门信息进行过滤
            queryset = self.filter_queryset(self.get_queryset().filter(department__in=permission_department_list))
        else:
            # 部门权限信息为空，只能查看到自身的数据
            queryset = self.filter_queryset(self.get_queryset().filter(id=user.id))
        return queryset

    def get_permissions_object(self, request):
        user = request.user
        # 如果当前部门权限信息为空，则表示没有为当前用户 角色 分配部门权限信息
        permission_department_list = user.get_permission_department_list()
        instance = self.get_object()
        # 每个用户都拥有操作自身数据的权利
        if instance == user:
            return instance
        if instance.department not in permission_department_list:
            # 当前用户所用于的部门操作权限，以及当前数据所在的部门
            raise PermissionDenied('你没有操作该部门数据的权限')
        return instance

    def list(self, request, *args, **kwargs):
        queryset = self.get_permissions_queryset(request)
        # 结果集分页
        page = self.paginate_queryset(queryset)
        result_data = self.get_serializer(page, many=True).data
        return Response(dict(self.get_paginated_response(result_data), **{"msg": "查询成功", "status": 1}))

    def retrieve(self, request, *args, **kwargs):
        # 查询指定对象的详情
        instance = self.get_permissions_object(request)
        result_data = self.get_serializer(instance).data
        return Response({"data": result_data, "msg": "查询成功", "status": 1})

    def create(self, request, *args, **kwargs):
        user = request.user
        req_data = request.data.copy()
        # 用户新增时，需要先判断当前新增的用户的部门参数，是否在可操作性的部门下
        # 如果当前没有传递部门信息，则当前用户所属的部门为 编号为1的对象【可能会有问题】
        if req_data.get('department'):
            department_list = user.get_permission_department_list()
            if req_data.get('department') not in [i.id for i in department_list]:
                raise PermissionError('你没有操作该部门数据的权限')
        if req_data.get('head_image'):
            req_data.pop('head_image')
        req_data['create_user'] = req_data['update_user'] = user.id  # 创建用户
        req_data['password'] = UserBase.set_password(req_data['password'])
        instance = self.add_instance(req_data, self.get_serializer_class(), user)
        return Response({"data": {'id': instance.id}, "msg": "新增成功", "status": 1})

    def update(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_permissions_object(request)
        req_data = request.data.copy()
        if req_data.get('password'):
            req_data['password'] = UserBase.set_password(req_data['password'])
        self.update_instance(req_data, self.get_serializer_class(), instance, user)
        return Response({'id': instance.id, "msg": "更新成功", "status": 1})

    def retrieve_person(self, request, *args, **kwargs):
        instance = request.user
        result_data = self.get_serializer(instance).data
        return Response({"data": result_data, "msg": "查询成功", "status": 1})

    def destroy(self, request, *args, **kwargs):
        # 删除指定对象，对应删除  role
        instance = self.get_permissions_object(request)
        instance.delete()
        return Response({"msg": "删除成功", "status": 1})


class MenuViewSet(BaseViewSet):
    queryset = Menu.objects.get_queryset().select_related("parent").prefetch_related("api").order_by('order_num')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ListMenuSerializer
        return MenuSerializer

    def get_permissions_queryset(self, request):
        user = request.user
        # 获取当前用户所拥有的所有的权限信息
        menus = user.get_menus_list()
        if menus:
            # 部门权限信息不为空，根据部门信息进行过滤
            queryset = self.filter_queryset(self.get_queryset().filter(pk__in=[i.id for i in menus]))
        else:
            # 部门权限信息为空，只能查看到自身的数据
            queryset = self.filter_queryset(self.get_queryset().filter(id=user.id))
        return queryset

    def get_permissions_object(self, request):
        user = request.user
        # 获取当前用户所拥有的所有的权限信息
        menus = user.get_menus_list()
        instance = self.get_object()
        if instance not in menus:
            raise PermissionError('数据权限不足')
        return instance

    def list(self, request, *args, **kwargs):
        # 查询包含分页的结果
        queryset = self.get_permissions_queryset(request)
        # 结果集分页
        page = self.paginate_queryset(queryset)
        result_data = self.get_serializer(page, many=True).data
        return Response(dict(self.get_paginated_response(result_data), **{'msg': '查询成功', "status": 1}))

    def retrieve(self, request, *args, **kwargs):
        # 查询指定对象的详情
        instance = self.get_permissions_object(request)
        result_data = self.get_serializer(instance).data
        return Response(dict(result_data, **{'msg': '查询成功', "status": 1}))

    def create(self, request, *args, **kwargs):
        user = request.user
        # role_list = user.get_role_list()
        req_data = request.data.copy()
        # 解决前端可能传递的parent信息为0的情况
        if req_data.get('parent') == 0:
            req_data.pop('parent')
        with transaction.atomic():
            instance = self.add_instance(req_data, self.get_serializer_class(), request.user)
            # 当前用户新增的菜单信息，可以被当前用户同角色的所有角色查看
            # instance.role.add(*role_list)
        return Response({"data": {"id": instance.id}, "msg": "新增成功", "status": 1})

    def destroy(self, request, *args, **kwargs):
        # 删除指定对象，需要级联删除所有的子对象
        instance = self.get_permissions_object(request)
        instance.delete()
        return Response({'msg': '删除成功', "status": 1})

    def perm_list(self, request, *args, **kwargs):
        # 指定用户的的权限列表，包含页面权限和数据权限
        user = request.user
        # 当前用户是超级管理员，直接返回所有的数据信息
        if request.auth:
            menu_list = Menu.objects.prefetch_related(
                Prefetch("api", to_attr="apis"),
            ).all()
            api_list = Api.objects.all()
        else:
            menu_list = user.get_menus_list()
            api_list = user.get_permission_api_list()
        menus = PermmenuMenuSerializer(menu_list, many=True).data
        perms = [i.format_path for i in api_list if i.format_path]
        return Response({"data": {'menus': menus, 'perms': perms}, 'msg': '查询成功', "status": 1})

    def test_list(self, request, *args, **kwargs):
        # 指定用户的的权限列表，包含页面权限和数据权限
        pass


class RoleViewSet(BaseViewSet):
    queryset = Role.objects.get_queryset().prefetch_related(
        Prefetch("menu"),
        Prefetch("department"),
    )

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ListRoleSerializer
        return RoleSerializer

    def list(self, request, *args, **kwargs):
        # 查询包含分页的结果
        queryset = self.filter_queryset(self.get_queryset())
        # 结果集分页
        page = self.paginate_queryset(queryset)
        result_data = self.get_serializer(page, many=True).data
        return Response(dict(self.get_paginated_response(result_data), **{"msg": "查询成功", "status": 1}))

    def create(self, request, *args, **kwargs):
        user = request.user
        req_data = request.data
        instance = self.add_instance(req_data, self.get_serializer_class(), user)
        return Response({'id': instance.id, 'msg': '新增成功', "status": 1})

    def retrieve(self, request, *args, **kwargs):
        # 查询角色详情
        instance = self.get_object()
        result_data = self.get_serializer(instance).data
        result_data['menu_id_list'] = result_data['menu_id_list'].split(',') if result_data['menu_id_list'] else []
        return Response(dict(result_data, **{'msg': '查询成功', "status": 1}))


class DepartmentViewSet(BaseViewSet):
    queryset = Department.objects.get_queryset().order_by('id')

    def get_serializer_class(self):
        return DepartmentSerializer


class ApiViewSet(BaseViewSet):
    queryset = Api.objects.get_queryset().order_by('id')

    def get_serializer_class(self):
        return ApiSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
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
            info['create_user'] = info['update_user'] = user.id
            info['format_path'] = info['path'].split('/api/')[1].replace('/', ':')
            if "common" in info['path']:
                info['is_common'] = 1
                info['format_path'] = ""
            add_api_list.append(Api(**info))
        Api.objects.bulk_create(add_api_list)
        return Response({'data': api_list, 'msg': '查询成功'})
