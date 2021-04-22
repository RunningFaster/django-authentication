from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination


class PaginationResponse(PageNumberPagination):
    page_size = 10  # 每页的记录数
    page_size_query_param = 'per_page'  # 获取url参数中设置的每页显示数据条数
    page_query_param = "page"  # 传递的参数：页码
    max_page_size = 100

    def get_paginated_response(self, data):
        paginator_data = {
            'paginator': {'count': self.page.paginator.count,
                          'page': self.page.number,
                          'num_pages': self.page.paginator.num_pages,
                          'per_page': self.page.paginator.per_page},
            'object_list': data
        }
        # 取消Response方便生成分页对象后，添加后续的处理逻辑
        return OrderedDict([
            ('data', paginator_data),
            # ('next', self.get_next_link()),
            # ('previous', self.get_previous_link()),
        ])
