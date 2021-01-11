# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : Friday
# @FILE     : base_model.py
# @Time     : 2021/1/11 14:36
# @Software : PyCharm

from django.db import models


class BaseModel(models.Model):
    create_datetime = models.DateTimeField("新增时间", auto_now_add=True, editable=False, db_index=True)
    create_user = models.IntegerField("创建者", blank=True)
    update_datetime = models.DateTimeField("最新修改时间", auto_now=True, editable=False, db_index=True)
    update_user = models.IntegerField("修改者", blank=True)

    class Meta:
        abstract = True
