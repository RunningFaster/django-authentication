import json
import traceback

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class GlobalMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        # 重写response，需要重新渲染
        response._is_rendered = False
        response.render()
        return response

    def process_exception(self, request, exception):
        # 异常 错误拦截接口，写入日志系统
        print('Exception:', exception)
        traceback.print_exc()
        return HttpResponse(json.dumps({'msg': exception.args}), status=400)
