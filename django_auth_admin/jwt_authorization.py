import time

from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import BasePermission
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from django.core.cache import cache

from users.models import Role, Menu, RoleUserBase, RoleDepartment, RoleMenu, Api, MenuApi


class RewriteVerifyJSONWebTokenSerializer(VerifyJSONWebTokenSerializer):
    """
    Check the veracity of an access token.
    """

    def validate(self, attrs):
        token = attrs['token']

        payload = self._check_payload(token=token)
        user = self._check_user(payload=payload)

        return {
            'token': token,
            'user': user,
            'payload': payload
        }


class JWTAuthentication(TokenAuthentication):

    def verify_token(self, token: str, payload: dict) -> bool:
        # 判断当前 token 的时间是否已过期
        if int(time.time()) > payload['exp']:
            return False
        # 判断当前 token 是否在 token 黑名单中
        cache_res = cache.get("auth-black:token:{}".format(token))
        if cache_res:
            return False
        return True

    def authenticate(self, request, **kwargs):
        is_refresh = True if "refresh" in request.path else False
        # JWT token 方式校验
        try:
            # 请求头中获取信息
            token = request.META['HTTP_AUTHORIZATION']
            serializer = RewriteVerifyJSONWebTokenSerializer(data={'token': token})
            serializer.is_valid(raise_exception=True)
            serializer_data = serializer.object
            if is_refresh:
                serializer_data['payload'].update({'refresh_token': token})
            else:
                serializer_data['payload']['token'] = token
            # 防止使用 refreshToken 进行数据请求
            if is_refresh != bool(serializer_data['payload'].get('refresh')):
                raise exceptions.AuthenticationFailed('认证失败')
            # 验证token当前是否有效
            if not self.verify_token(serializer_data['token'].split('.')[2], serializer_data['payload']):
                raise exceptions.AuthenticationFailed('认证失败')
        except Exception:
            raise exceptions.AuthenticationFailed('认证失败')
        return serializer_data['user'], serializer_data['payload']


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        """
        超级管理员角色，只能操作
        """
        user = request.user
        if user:
            return True
        try:
            # 当前接口如果最后一位是可变参数，则需要排除掉此部分
            int(request.path[-1])
            req_path = "/".join(request.path.split('/')[:-1])
        except ValueError:
            req_path = request.path
        if "common" in req_path:
            # 通用接口，不受到权限的控制
            return True

        # 查询当前用户所拥有的 角色
        role_id_list = list(RoleUserBase.objects.values_list("role", flat=True).filter(user_base=user.id))
        if 1 not in role_id_list:
            # 超级管理员不受到权限控制
            return True

        # 接口权限过滤，判断当前用户是否拥有当前接口的操作权限
        try:
            api_instance = Api.objects.get(path=req_path, method=request.META['REQUEST_METHOD'])
        except Api.DoesNotExist:
            raise exceptions.PermissionDenied()
        # 查询当前角色 所拥有的的所有的权限信息
        menu_id_list = list(set(list(RoleMenu.objects.values_list("menu", flat=True).filter(role__in=role_id_list))))
        if not menu_id_list:
            return False
        # 查询 所有权限对应的 API 的信息
        apis = MenuApi.objects.values_list("api", flat=True).filter(menu__in=menu_id_list)
        if api_instance.id not in apis:
            return False
        return True
