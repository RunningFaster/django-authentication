import time

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db.models import Prefetch
from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed, MethodNotAllowed
from rest_framework.permissions import BasePermission
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from django.core.cache import cache

User = get_user_model()


class RewriteVerifyJSONWebTokenSerializer(VerifyJSONWebTokenSerializer):
    """
    Check the veracity of an access token.
    """

    def _check_user(self, payload):
        try:
            """
            认证获取用户阶段，把用户所属的信息进行提前量缓存
                role: 角色信息
                role__menu__api: 用户所拥有的所有的api信息
                role__department: 用户所在的部门信息
            """
            user = User.objects.select_related("department").prefetch_related(
                Prefetch("role__menu__api", to_attr="apis"),
                Prefetch("role__department", to_attr="departments"),
            ).get(username=payload['username'])
        except User.DoesNotExist:
            msg = "User doesn't exist."
            raise serializers.ValidationError(msg)

        if not user.is_active:
            msg = 'User account is disabled.'
            raise serializers.ValidationError(msg)

        return user

    def validate(self, attrs):
        token = attrs['token']

        payload = self._check_payload(token=token)
        user = self._check_user(payload=payload)
        # 更改返回 token 信息
        return {
            'token': token,
            'user': user,
            'payload': payload
        }


class JWTAuthentication(TokenAuthentication):

    @staticmethod
    def verify_token(token: str, payload: dict) -> bool:
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
            token = request.META['HTTP_AUTHORIZATION']
            # 处理通用接口
            serializer = RewriteVerifyJSONWebTokenSerializer(
                data={'token': token})
            serializer.is_valid(raise_exception=True)
            serializer_data = serializer.object
            if is_refresh:
                serializer_data['payload'].update({'refresh_token': token})
            else:
                serializer_data['payload']['token'] = token
            # 防止使用 refreshToken 进行数据请求
            if is_refresh != bool(serializer_data['payload'].get('refresh')):
                raise AuthenticationFailed('认证失败')
            # 验证当前token是否在黑名单
            if not self.verify_token(serializer_data['token'].split('.')[2], serializer_data['payload']):
                raise AuthenticationFailed('认证失败')
        except Exception:
            raise AuthenticationFailed('认证失败')
        # 用户对象 和 权限信息
        user = serializer_data['user']
        is_superuser = True
        return user, is_superuser


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        """
        超级管理员角色，只能操作
        """
        user = request.user
        if isinstance(user, AnonymousUser):
            return False
        # 当前api操作是否是针对指定对象的操作
        try:
            # 当前接口如果最后一位是可变参数，则需要排除掉此部分
            int(request.path[-1])
            req_path = "/".join(request.path.split('/')[:-1])
        except ValueError:
            req_path = request.path
        if "common" in req_path:
            # 通用接口，不受到权限的控制
            return True
        # 查询当前角色所拥有的权限信息，以及权限对应的api的信息
        api_list = user.get_permission_api_list()
        # 接口权限过滤，判断当前用户是否拥有当前接口的操作权限
        for api in api_list:
            if req_path == api.path:
                if request.META['REQUEST_METHOD'] != api.method:
                    raise MethodNotAllowed(request.META['REQUEST_METHOD'])
                return True
        return False
