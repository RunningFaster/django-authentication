from django.urls import include, path
from users.urls import user_urlpatterns, menu_urlpatterns, common_urlpatterns

urlpatterns = [
    path(r'api/sys/user/', include(user_urlpatterns), name="用户"),
    path(r'api/sys/menu/', include(menu_urlpatterns)),
    # 系统级别接口，不受权限控制，通用权限
    path(r'api/common/', include(common_urlpatterns)),
]
