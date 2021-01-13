import json
import traceback

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class GlobalMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        # response._is_rendered = False
        # response.status_code = 200
        # response.render()
        return response

    def process_exception(self, request, exception):
        # 异常 错误拦截接口，写入日志系统
        print('Exception:', exception)
        traceback.print_exc()
        return HttpResponse(json.dumps({'msg': exception.args}), status=400)
