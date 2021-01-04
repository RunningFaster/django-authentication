# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : Friday
# @FILE     : utils.py
# @Time     : 2021/1/4 13:32
# @Software : PyCharm


def jwt_get_user_secret(user):
    # 指定生成用户 jwt token 的加密密钥参数，针对如果用户进行密码修改，则该用户之前的所有的 token 都将失效
    return user.password
