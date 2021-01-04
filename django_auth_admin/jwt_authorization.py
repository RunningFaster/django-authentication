import time

from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import BasePermission
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from django.core.cache import cache


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
        # 已经登陆，可以直接从request里面获取用户对象
        user = request.user
        if user:
            return True
        return False
