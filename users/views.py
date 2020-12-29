from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from django_auth_admin.jwt_middleware import JWTAuthentication, AdminPermission
from users.models import UserBase
from users.serializers import ListUserBaseSerializer, UserBaseSerializer


class LoginViewSet(viewsets.ModelViewSet):
    queryset = UserBase.objects.get_queryset()
    authentication_classes = ()
    permission_classes = ()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ListUserBaseSerializer
        return UserBaseSerializer

    def login(self, request, *args, **kwargs):
        req_data = request.data
        username = req_data.get('username')
        password = req_data.get('password')
        if not username or not password:
            return Response({"status": 0, "msg": "参数校验错误"})
        instance_list = UserBase.objects.filter(username=req_data['username'])
        if not len(instance_list):
            return Response({"status": 0, "msg": "登陆失败，用户名不存在"})
        instance = instance_list.first()
        if not instance.check_password(password):
            Response({"status": 0, "msg": "登陆失败，密码错误"})
        if instance.is_active:
            return Response({"status": 0, "msg": "账户状态异常，无法登陆，请联系管理员"})
        # 根据user对象信息生成token
        payload = jwt_payload_handler(instance)
        token = jwt_encode_handler(payload)
        return Response({"status": 1, "msg": "success", "data": {'expire': 3600, 'token': token}})


class UserBaseViewSet(LoginViewSet):
    queryset = UserBase.objects.get_queryset()

    # authentication_classes = (JWTAuthentication,)
    # permission_classes = (AdminPermission,)

    def create(self, request, *args, **kwargs):
        req_data = request.data.copy()
        req_data['create_user'] = 1
        req_data['update_user'] = 1
        serializer = self.get_serializer(data=req_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"status": 1, "msg": "成功", 'data': serializer.data})
