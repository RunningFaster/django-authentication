# 开发部Rj对应路由地址
from django.urls import path

from users import views

common_urlpatterns = [
    path(r'login', views.TokenViewSet.as_view({'post': 'login'}), name="登录"),
    path(r'logout', views.AuthTokenViewSet.as_view({'post': 'logout'}), name="退出登录"),
    path(r'refresh', views.AuthTokenViewSet.as_view({'post': 'refresh'}), name="刷新认证"),

    path(r'district/list', views.DistrictViewSet.as_view({'get': 'list'}), name="区列表"),
    path(r'street/list', views.StreetViewSet.as_view({'get': 'list'}), name="街道列表"),
    path(r'committee/list', views.CommitteeViewSet.as_view({'get': 'list'}), name="居委列表"),

    path(r'api/list', views.ApiViewSet.as_view({'get': 'list'}), name="接口列表"),
]

user_urlpatterns = [
    path(r'list', views.UserBaseViewSet.as_view({'get': 'list'}), name="用户列表"),
    path(r'info/<int:pk>', views.UserBaseViewSet.as_view({'get': 'retrieve'}), name="用户详情"),
    path(r'add', views.UserBaseViewSet.as_view({'post': 'create'}), name="新增用户"),
    path(r'delete/<int:pk>', views.UserBaseViewSet.as_view({'post': 'destroy'}), name="删除用户"),
    path(r'update/<int:pk>', views.UserBaseViewSet.as_view({'post': 'update'}), name="更新用户"),
]

menu_urlpatterns = [
    path(r'list', views.MenuViewSet.as_view({'get': 'list'})),
    path(r'info/<int:pk>', views.MenuViewSet.as_view({'get': 'retrieve'})),
    path(r'add', views.MenuViewSet.as_view({'post': 'create'})),
    path(r'delete/<int:pk>', views.MenuViewSet.as_view({'post': 'destroy'})),
    path(r'update/<int:pk>', views.MenuViewSet.as_view({'post': 'update'})),
]
