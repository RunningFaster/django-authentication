# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : Friday
# @FILE     : base_swagger.py
# @Time     : 2021/1/13 17:02
# @Software : PyCharm

from drf_yasg.inspectors import SwaggerAutoSchema


class CustomSwaggerAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        tags = super().get_tags(operation_keys)

        if "sys" in tags and operation_keys:
            #  `operation_keys` 内容像这样 ['v1', 'prize_join_log', 'create']
            tags[0] = operation_keys[1]

        return tags
