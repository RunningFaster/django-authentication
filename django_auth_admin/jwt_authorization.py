import time

from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import BasePermission
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from django.core.cache import cache

from users.models import Role, Menu


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
        user = request.user
        if user:
            return True
        # 处理当前路由上的可变参数信息
        try:
            int(request.path[-1])
            req_path = "/".join(request.path.split('/')[2:-1]).replace('/', ':')
        except ValueError:
            req_path = request.path.split('/api/')[1].replace('/', ':')
        if "common" in req_path:
            # 通用接口，不受到任何权限的限制
            return True
        # 第一层判断：接口权限过滤，判断当前用户是否拥有当前接口的操作权限
        menu_id_list = list(set(",".join(list(Role.objects.values_list('menu_id_list', flat=True).filter(
            pk__in=user.role_id_list.split(',')))).split(",")))
        if not len(menu_id_list):
            return False
        menu_instance_list = Menu.objects.filter(pk__in=menu_id_list)
        perms = list(
            set(",".join(list(menu_instance_list.values_list("perms", flat=True).filter(type=2))).split(',')))
        if req_path not in perms:
            return False
        # 第二次过滤：数据权限过滤，需要根据当前用户属于哪个部门进行数据过滤，
        return True
