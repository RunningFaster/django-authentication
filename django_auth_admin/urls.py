from django.urls import include, path
from users.urls import user_urlpatterns, menu_urlpatterns, common_urlpatterns, role_urlpatterns

urlpatterns = [
    # 普通接口
    path(r'api/sys/user/', include(user_urlpatterns), name="用户"),
    path(r'api/sys/menu/', include(menu_urlpatterns), name="权限"),
    path(r'api/sys/role/', include(role_urlpatterns), name="角色"),
    # 系统级别接口，不受权限控制，通用权限，common涉及到 权限判断，该字段不能替换
    path(r'api/common/', include(common_urlpatterns), name="通用"),
]
