#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author:wd
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_authentication.settings.pro')  # 设置django环境

app = Celery('django_authentication')

app.config_from_object('django.conf:settings')  # 使用CELERY_ 作为前缀，在settings中写配置

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)  # 发现任务文件每个app下的task.py

"""
启动命令行：
# 启动worker任务进程
python manage.py celery worker -l info -P eventlet -c 10
# 启动beat监护进程
celery beat -A django_authentication -l info
# 启动flower界面化
celery flower -A django_authentication --address=0.0.0.0 --port=9108

# 杀调进程
ps -aux | grep celery | grep -v grep | grep pro | cut -c 9-15 | xargs kill -9
"""