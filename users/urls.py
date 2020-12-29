# 开发部Rj对应路由地址
from django.urls import path

from users import views

app_name = '[users]'

urlpatterns = [
    path(r'login/', views.LoginViewSet.as_view({'post': 'login'})),
    path(r'logout/', views.LoginViewSet.as_view({'post': 'logout'})),
]

urlpatterns += [
    path(r'list/', views.UserBaseViewSet.as_view({'get': 'list'})),
    path(r'info/<int:pk>/', views.UserBaseViewSet.as_view({'get': 'retrieve'})),
    path(r'add/', views.UserBaseViewSet.as_view({'post': 'create'})),
    path(r'delete/', views.UserBaseViewSet.as_view({'post': 'destroy'})),
    path(r'update/', views.UserBaseViewSet.as_view({'post': 'update'})),
]
