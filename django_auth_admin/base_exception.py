# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : Friday
# @FILE     : base_exception.py
# @Time     : 2021/1/14 16:31
# @Software : PyCharm


from django.core.exceptions import ValidationError
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response


def common_exception_handler(exc, context):
    msg = "请求失败"
    status_code = status.HTTP_200_OK
    if isinstance(exc, Http404):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, MethodNotAllowed):
        status_code = status.HTTP_403_FORBIDDEN
    elif isinstance(exc, ValidationError):
        msg = "".join(["{}-{}".format(str(key), str(value[0])) for key, value in exc.message_dict.items()])
    else:
        # 在此处补充自定义的异常处理
        print('[%s]: %s' % (context['view'], exc))
        msg = max("".join(getattr(exc, "args")), "".join(getattr(exc, "detail")))
    data = {"status": 0, "msg": msg}
    response = Response(data, status=status_code)
    return response
