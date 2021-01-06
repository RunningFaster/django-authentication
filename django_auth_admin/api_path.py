# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : Friday
# @FILE     : api_path.py
# @Time     : 2021/1/4 15:21
# @Software : PyCharm

import re
from importlib import import_module

from rest_framework.views import APIView

from django.utils import six
from django.contrib.admindocs.views import simplify_regex
from django.conf import settings
from django.urls import URLPattern, URLResolver


class API_PATH:
    """
    获取本项目的API列表
    """

    _PATH_PARAMETER_COMPONENT_RE = re.compile(r'<(?:(?P<converter>[^>:]+):)?(?P<parameter>\w+)>')

    def get_apis(self):
        data = []

        urlconf = settings.ROOT_URLCONF

        if not isinstance(urlconf, six.string_types):
            return []

        urls = import_module(urlconf)

        patterns = urls.urlpatterns

        data = self.__get_api_endpoints(patterns)
        return data

    def __is_api_view(self, callback):
        """
        如果给定的视图回调是DRF View/viewset，则返回True
        """
        cls = getattr(callback, 'cls', None)
        return (cls is not None) and issubclass(cls, APIView)

    def endpoint_ordering(self, endpoint):
        """
        返回排序字段
        :param endpoint:
        :return:
        """
        #todo: 新增返回字段信息
        path, method, name = endpoint.values()
        method_priority = {
            'GET': 0,
            'POST': 1,
            'PUT': 2,
            'PATCH': 3,
            'DELETE': 4
        }.get(method, 5)
        return (path, method_priority)

    def __get_path_from_regex(self, path_regex):
        """
        给定URL conf正则表达式，返回URI模板字符串
        """
        path = simplify_regex(path_regex)
        path = re.sub(self._PATH_PARAMETER_COMPONENT_RE, r'{\g<parameter>}', path)
        return path

    def __should_include_endpoint(self, path, callback):
        """
        如果应该包含给定的endpoint，则返回“ True”
        """
        if not self.__is_api_view(callback):
            return False

        if callback.cls.schema is None:
            return False

        if 'schema' in callback.initkwargs:
            if callback.initkwargs['schema'] is None:
                return False

        if path.endswith('.{format}') or path.endswith('.{format}/'):
            return False

        return True

    def __get_allowed_methods(self, callback):
        """
        返回允许的http method列表
        """
        if hasattr(callback, 'actions'):
            actions = set(callback.actions)
            http_method_names = set(callback.cls.http_method_names)
            methods = [method.upper() for method in actions & http_method_names]
        else:
            methods = callback.cls().allowed_methods

        return [method for method in methods if method not in ('OPTIONS', 'HEAD')]

    def __get_api_endpoints(self, patterns=None, prefix=''):
        """
        通过检查URL conf返回所有可用API端点的列表
        """
        if patterns is None:
            patterns = patterns

        api_endpoints = []

        for pattern in patterns:
            # path_regex = prefix + get_original_route(pattern)
            path_regex = prefix + pattern.pattern.regex.pattern.replace('\\', '')
            if isinstance(pattern, URLPattern):
                path = self.__get_path_from_regex(path_regex)
                callback = pattern.callback
                if self.__should_include_endpoint(path, callback):
                    for method in self.__get_allowed_methods(callback):
                        endpoint = {"path": path.replace("/{pk}", ""),
                                    # "describe": str(callback.initkwargs['description']).strip().split('\n')[0] if
                                    # callback.initkwargs.get('description') else
                                    # str(callback.__doc__).strip().split('\n')[0],
                                    #todo: 从 name 中获取备注信息
                                    "name": pattern.name,
                                    "method": method}
                        api_endpoints.append(endpoint)

            elif isinstance(pattern, URLResolver):
                nested_endpoints = self.__get_api_endpoints(
                    patterns=pattern.url_patterns,
                    prefix=path_regex
                )
                api_endpoints.extend(nested_endpoints)

        api_endpoints = sorted(api_endpoints, key=self.endpoint_ordering)

        return api_endpoints


if __name__ == '__main__':
    api = API_PATH()
    apis = api.get_apis()
    for i in apis:
        print(i)
