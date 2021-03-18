# !/usr/bin/settings Python3
# -*- coding: utf-8 -*-
# @Author   : Friday
# @FILE     : base_viewset.py
# @Time     : 2021/1/11 14:37
# @Software : PyCharm
import json

from django.core import exceptions
from rest_framework import viewsets
from rest_framework.response import Response

from url_filter.integrations.drf import DjangoFilterBackend


class BaseViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filter_fields = "__all__"
    ordering_fields = "__all__"
    search_fields = "__all__"

    def get_permissions_queryset(self, request):
        # 用户可操作对象集合
        return True

    def get_permissions_object(self, request):
        # 用户可操作对象，如果权限不足，则返回403
        return True

    def list(self, request, *args, **kwargs):
        # 查询包含分页的结果
        queryset = self.filter_queryset(self.get_queryset())
        # 结果集分页
        page = self.paginate_queryset(queryset)
        result_data = self.get_serializer(page, many=True).data
        return Response(dict(self.get_paginated_response(result_data), **{"msg": "查询成功", "status": 1}))

    def list_without_paginate(self, request, *args, **kwargs):
        # 查询不包含分页的结果
        queryset = self.filter_queryset(self.get_queryset())
        result_data = self.get_serializer(queryset, many=True).data
        return Response(dict(result_data, **{"msg": "查询成功", "status": 1}))

    def retrieve(self, request, *args, **kwargs):
        # 查询指定对象的详情
        instance = self.get_object()
        result_data = self.get_serializer(instance).data
        return Response(dict(result_data, **{"msg": "查询成功", "status": 1}))

    def create(self, request, *args, **kwargs):
        req_data = request.data.copy()
        instance = self.add_instance(req_data, self.get_serializer_class(), request.user)
        return Response({"id": instance.id, "msg": "新增成功", "status": 1})

    def update(self, request, *args, **kwargs):
        # 更新对象
        instance = self.get_object()
        req_data = request.data.copy()
        self.update_instance(req_data, self.get_serializer_class(), instance, request.user)
        return Response({"id": instance.id, "msg": "更新成功", "status": 1})

    def destroy(self, request, *args, **kwargs):
        # 删除指定对象，当前删除为硬删除，直接在数据库中进行删除处理
        instance = self.get_object()
        instance.delete()
        return Response({"msg": "删除成功", "status": 1})

    @staticmethod
    def update_instance(data: dict, serializer, instance, user):
        # 更新对象
        data["update_user"] = user.id
        serializer = serializer(instance, data, partial=True)
        result_bool = serializer.is_valid(raise_exception=False)
        if not result_bool:
            raise exceptions.ValidationError(serializer.errors)
        serializer.save()
        return instance

    @staticmethod
    def add_instance(data: dict, serializer, user):
        # 新增对象
        data["create_user"] = user.id
        data["update_user"] = user.id
        serializer = serializer(data=data)
        result_bool = serializer.is_valid(raise_exception=False)
        if not result_bool:
            raise exceptions.ValidationError(serializer.errors)
        instance = serializer.save()
        return instance
