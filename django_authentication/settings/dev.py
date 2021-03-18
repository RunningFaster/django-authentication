# !/usr/bin/settings Python3
# -*- coding: utf-8 -*-
# @Author   : Friday
# @FILE     : dev.py
# @Time     : 2021/3/18 16:22
# @Software : PyCharm

from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django-authentication',
    }
}

