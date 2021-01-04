import json
import traceback

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response


class GlobalMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        status_code = str(response.status_code)
        if isinstance(response, Response) and status_code != '405':
            status = 1
            msg = ''
            data_dict = {}
            # 如果后台错误，则处理错误信息
            if isinstance(response.data, str) or status_code.startswith('4'):
                status = 0
                msg = response.data.get('detail', json.dumps(response.data, ensure_ascii=False)) if isinstance(
                    response.data, dict) else response.data
            # 数据进行包装，如果结果有 data 参数，则不用二次包裹
            elif response.data:
                data_dict = response.data if response.data.get('data') else {'data': response.data}
                # 处理msg信息
                msg = response.data.pop('msg') if response.data.get('msg') else 'success'
            response.data = dict({'status': status, 'msg': msg}, **data_dict)
            # 强行修改 response 对象内容，需要进行重新渲染操作
            response._is_rendered = False
            response.status_code = 200
            response.render()
        return response

    def process_exception(self, request, exception):
        # 异常 错误拦截接口，写入日志系统
        print('Exception:', exception)
        traceback.print_exc()
        return HttpResponse(json.dumps({'msg': exception.args}), status=400)
