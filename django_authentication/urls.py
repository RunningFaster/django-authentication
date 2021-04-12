from django.urls import include, path
import debug_toolbar
from rest_framework.documentation import include_docs_urls

from organization.urls import user_urlpatterns, menu_urlpatterns, common_urlpatterns, role_urlpatterns, \
    department_urlpatterns
from django.contrib import admin

urlpatterns = [
    # 普通接口
    path(r'api/sys/user/', include(user_urlpatterns), name="用户"),
    path(r'api/sys/menu/', include(menu_urlpatterns), name="权限"),
    path(r'api/sys/role/', include(role_urlpatterns), name="角色"),
    path(r'api/sys/department/', include(department_urlpatterns), name="部门"),
    # 系统级别接口，不受权限控制，通用权限，common涉及到 权限判断，该字段不能替换
    path(r'api/common/', include(common_urlpatterns), name="通用"),
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title="组织架构")),
]
