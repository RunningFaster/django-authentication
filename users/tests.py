from django.test import TestCase

# Create your tests here.

a = {
    "status": 1,
    "msg": "查询成功",
    "data": [
        {
            "api": "/api/common/api/list",
            "name": "后台接口列表",
            "method": "GET"
        },
        {
            "api": "/api/common/committee/list",
            "name": "居委列表",
            "method": "GET"
        },
        {
            "api": "/api/common/district/list",
            "name": "区列表",
            "method": "GET"
        },
        {
            "api": "/api/common/login",
            "name": "登录",
            "method": "POST"
        },
        {
            "api": "/api/common/logout",
            "name": "退出登录",
            "method": "POST"
        },
        {
            "api": "/api/common/permmenu",
            "name": "用户权限列表",
            "method": "GET"
        },
        {
            "api": "/api/common/refresh",
            "name": "刷新认证",
            "method": "POST"
        },
        {
            "api": "/api/common/street/list",
            "name": "街道列表",
            "method": "GET"
        },
        {
            "api": "/api/sys/menu/add",
            "name": "新增权限",
            "method": "POST"
        },
        {
            "api": "/api/sys/menu/delete",
            "name": "删除权限",
            "method": "POST"
        },
        {
            "api": "/api/sys/menu/info",
            "name": "权限详情",
            "method": "GET"
        },
        {
            "api": "/api/sys/menu/list",
            "name": "权限列表",
            "method": "GET"
        },
        {
            "api": "/api/sys/menu/update",
            "name": "更新权限",
            "method": "POST"
        },
        {
            "api": "/api/sys/role/add",
            "name": "新增角色",
            "method": "POST"
        },
        {
            "api": "/api/sys/role/delete",
            "name": "删除角色",
            "method": "POST"
        },
        {
            "api": "/api/sys/role/info",
            "name": "角色详情",
            "method": "GET"
        },
        {
            "api": "/api/sys/role/list",
            "name": "角色列表",
            "method": "GET"
        },
        {
            "api": "/api/sys/role/update",
            "name": "更新角色",
            "method": "POST"
        },
        {
            "api": "/api/sys/user/add",
            "name": "新增用户",
            "method": "POST"
        },
        {
            "api": "/api/sys/user/delete",
            "name": "删除用户",
            "method": "POST"
        },
        {
            "api": "/api/sys/user/info",
            "name": "用户详情",
            "method": "GET"
        },
        {
            "api": "/api/sys/user/list",
            "name": "用户列表",
            "method": "GET"
        },
        {
            "api": "/api/sys/user/update",
            "name": "更新用户",
            "method": "POST"
        }
    ]
}
c = []
for i in a['data']:
    if "common" in i['api']:
        continue
    c.append(i['api'].split('/api/')[1].replace("/", ":"))

print(','.join(c))