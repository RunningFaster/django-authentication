from django.utils.deprecation import MiddlewareMixin

from django.core.cache import cache
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import BasePermission
from rest_framework_jwt.authentication import jwt_decode_handler


class ErrorHandlingMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        return response


class JWTAuthentication(TokenAuthentication):
    def authenticate(self, request, **kwargs):
        # JWT token 方式校验
        try:
            # 请求头中获取信息
            token = request.META['HTTP_AUTHORIZATION']
            print("获取到的Token为 {}".format(token))
            # 解析jwt token 信息，获取到token中加密的详细信息
            payload = jwt_decode_handler(token)
            print("payload:", payload)
        except Exception:
            raise exceptions.AuthenticationFailed({'result': 2, 'msg': '认证失败'})
        cache.set("cn-{}-auth".format(payload['id']), token)
        # 到redis查询当前认证是否过期
        new_token = cache.get("cn-{}-auth".format(payload['id']))
        # 如果当前数据没有获取到 new_token 说明当前token已过期
        if not new_token:
            raise exceptions.AuthenticationFailed({'result': 2, 'msg': '认证失败'})
        # 此处返回的 payload 就是用户对象，等同于 request.user 可以通过设定的属性获取到对应的值
        return payload, token


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        # 已经登陆，可以直接从request里面获取用户对象
        user = request.user
        if user:
            return True
        return False
