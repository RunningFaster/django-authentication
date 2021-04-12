# Readme

## 项目说明

* 本项目为基于django的认证和权限系统
* 认证使用 JWT，包含token发放和token refresh，token主动失效
* 权限包含路由权限和接口权限

## 文件夹目录介绍

> 获取当前Django项目所有的api

* basic -> api_path.py

> 自定义分页

* basic -> page_pagination.py

> 自定义认证

* basic -> base_authorization.py

> 自定义全局异常

* basic -> base_exception.py

## 项目启动

> 安装环境

```shell script
pip3 install -r requirment.txt
```

> 添加mysql配置信息

settings/dev.py

> 执行迁移命令

```shell script
python manage.py makemigrations
python manage.py migrate
```

### ERP

> 模型关系图

https://github.com/RunningFaster/django-authentication/blob/master/static/github/ERP.png
![image](https://github.com/RunningFaster/django-authentication/blob/master/static/github/ERP.png)

### 认证

> jwt认证流程图
http://assets.processon.com/chart_image/5feac0091e08531ceabbd41d.png
![设计图](http://assets.processon.com/chart_image/5feac0091e08531ceabbd41d.png)

### 权限

### 更新

### 待更新

* Menu 和 Department 使用mptt进行树形结构优化