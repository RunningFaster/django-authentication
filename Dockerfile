FROM python:3.7.2

MAINTAINER Jamie <ren@126.com>

# 设置python环境变量
ENV PYTHONUNBUFFERED 1

# 在容器内创建文件夹
RUN mkdir -p /var/www/html/django-authorization

# 设置容器内的工作目录
WORKDIR /var/www/html/django-authorization

# 将当前目录内的文件拷贝的容器的工作目录中
ADD . /var/www/html/django-authorization

# 更新pip版本 和 安装依赖
RUN /usr/local/bin/python3 -m pip3 install --upgrade pip && pip3 install -r requirement.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 设置start.sh文件的可执行权限
RUN chmod +x ./start.sh