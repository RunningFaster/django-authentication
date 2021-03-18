# 开发部Rj对应路由地址
from django.urls import path

from organization import views

# 通用接口，不在权限分配管理系统中
common_urlpatterns = [
    path(r'login', views.TokenViewSet.as_view({'post': 'login'}), name="登录"),
    path(r'logout', views.AuthTokenViewSet.as_view({'post': 'logout'}), name="退出登录"),
    path(r'refresh', views.AuthTokenViewSet.as_view({'post': 'refresh'}), name="刷新认证"),
    path(r'person', views.UserBaseViewSet.as_view({'get': 'retrieve_person'}), name="当期用户详情"),

    path(r'permmenu', views.MenuViewSet.as_view({'get': 'perm_list'}), name="用户权限列表"),
    path(r'api/list', views.ApiViewSet.as_view({'get': 'list'}), name="后台接口列表"),
]

# 业务接口，通常根据角色进行对应的分配
# todo: 数据层面的 分割，以什么形式进行参数可配式架构
user_urlpatterns = [
    path(r'list', views.UserBaseViewSet.as_view({'get': 'list'}), name="用户列表"),
    path(r'info/<int:pk>', views.UserBaseViewSet.as_view({'get': 'retrieve'}), name="用户详情"),
    path(r'add', views.UserBaseViewSet.as_view({'post': 'create'}), name="新增用户"),
    path(r'delete/<int:pk>', views.UserBaseViewSet.as_view({'post': 'destroy'}), name="删除用户"),
    path(r'update/<int:pk>', views.UserBaseViewSet.as_view({'post': 'update'}), name="更新用户"),
]

menu_urlpatterns = [
    path(r'list', views.MenuViewSet.as_view({'get': 'list'}), name="权限列表"),
    path(r'test_list', views.MenuViewSet.as_view({'get': 'test_list'}), name="权限列表"),
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

department_urlpatterns = [
    path(r'list', views.DepartmentViewSet.as_view({'get': 'list'}), name="部门列表"),
    path(r'info/<int:pk>', views.DepartmentViewSet.as_view({'get': 'retrieve'}), name="部门详情"),
    path(r'add', views.DepartmentViewSet.as_view({'post': 'create'}), name="新增部门"),
    path(r'delete/<int:pk>', views.DepartmentViewSet.as_view({'post': 'destroy'}), name="删除部门"),
    path(r'update/<int:pk>', views.DepartmentViewSet.as_view({'post': 'update'}), name="更新部门"),
]
