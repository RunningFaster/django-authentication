# 开发部Rj对应路由地址
from django.urls import path

from users import views

# 通用接口，不在权限分配管理系统中
common_urlpatterns = [
    path(r'login', views.TokenViewSet.as_view({'post': 'login'}), name="登录"),
    path(r'logout', views.AuthTokenViewSet.as_view({'post': 'logout'}), name="退出登录"),
    path(r'refresh', views.AuthTokenViewSet.as_view({'post': 'refresh'}), name="刷新认证"),
    path(r'person', views.UserBaseViewSet.as_view({'get': 'retrieve_person'}), name="当期用户详情"),

    path(r'district/list', views.DistrictViewSet.as_view({'get': 'list'}), name="区列表"),
    path(r'street/list', views.StreetViewSet.as_view({'get': 'list'}), name="街道列表"),
    path(r'committee/list', views.CommitteeViewSet.as_view({'get': 'list'}), name="居委列表"),

    path(r'permmenu', views.MenuViewSet.as_view({'get': 'perm_list'}), name="用户权限列表"),
    path(r'api/list', views.ApiViewSet.as_view({'get': 'list'}), name="后台接口列表"),
]

user_urlpatterns = [
    path(r'list', views.UserBaseViewSet.as_view({'get': 'list'}), name="用户列表"),
    path(r'info/<int:pk>', views.UserBaseViewSet.as_view({'get': 'retrieve'}), name="用户详情"),
    path(r'add', views.UserBaseViewSet.as_view({'post': 'create'}), name="新增用户"),
    path(r'delete/<int:pk>', views.UserBaseViewSet.as_view({'post': 'destroy'}), name="删除用户"),
    path(r'update/<int:pk>', views.UserBaseViewSet.as_view({'post': 'update'}), name="更新用户"),
]

menu_urlpatterns = [
    path(r'list', views.MenuViewSet.as_view({'get': 'list'}), name="权限列表"),
    path(r'info/<int:pk>', views.MenuViewSet.as_view({'get': 'retrieve'}), name="权限详情"),
    path(r'add', views.MenuViewSet.as_view({'post': 'create'}), name="新增权限"),
    path(r'delete/<int:pk>', views.MenuViewSet.as_view({'post': 'destroy'}), name="删除权限"),
    path(r'update/<int:pk>', views.MenuViewSet.as_view({'post': 'update'}), name="更新权限"),
]

role_urlpatterns = [
    path(r'list', views.RoleViewSet.as_view({'get': 'list'}), name="角色列表"),
    path(r'info/<int:pk>', views.RoleViewSet.as_view({'get': 'retrieve'}), name="角色详情"),
    path(r'add', views.RoleViewSet.as_view({'post': 'create'}), name="新增角色"),
    path(r'delete/<int:pk>', views.RoleViewSet.as_view({'post': 'destroy'}), name="删除角色"),
    path(r'update/<int:pk>', views.RoleViewSet.as_view({'post': 'update'}), name="更新角色"),
]
