from django.conf.urls import url
from django.urls import include, path
import debug_toolbar
from users.urls import user_urlpatterns, menu_urlpatterns, common_urlpatterns, role_urlpatterns, department_urlpatterns
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # 普通接口
    path(r'api/sys/user/', include(user_urlpatterns), name="用户"),
    path(r'api/sys/menu/', include(menu_urlpatterns), name="权限"),
    path(r'api/sys/role/', include(role_urlpatterns), name="角色"),
    path(r'api/sys/department/', include(department_urlpatterns), name="部门"),
    # 系统级别接口，不受权限控制，通用权限，common涉及到 权限判断，该字段不能替换
    path(r'api/common/', include(common_urlpatterns), name="通用"),
    path('__debug__/', include(debug_toolbar.urls)),
]

urlpatterns += [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='文档json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='文档ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='文档新装饰'),
]
