#!/usr/bin/env bash
# 主服务
PROJECT_HOST="0.0.0.0"
# 主服务端口号
PROJECT_PORT="10005"
# Mysql连接
MYSQL_HOST="127.0.0.1"
MYSQL_PORT=10010
MYSQL_USER="root"
MYSQL_PASSWORD="toor"
MYSQL_DB="jingan_investment_dev"
# Redis连接
REDIS_HOST="127.0.0.1"
REDIS_PORT=10009
REDIS_PASSWORD=""
REDIS_DB=10
# 接口请求
ENV_ADDRESS_TO_LOCAL_URL="http://mapping.chinadigitalcity.com/api/address/location/"
ENV_LOCAL_TO_STREET_URL="http://mapping.chinadigitalcity.com/api/location/town/"
# Python环境地址
PYTHON_ENV="/home/renjing/.virtualenvs/DjangoAuthAdmin/bin"
# Django ENV
DJANGO_DEBUG=1


# ======上方需要根据上线环境手动修改配置=======

DIR=$(cd $(dirname $0) && pwd )
PROJECT_NAME="django_auth_admin"
LOG_PATH="/tmp/${PROJECT_NAME}.uwsgi.log"
DEV_CONFIG="${DIR}/${PROJECT_NAME}/env/pro.py"
# 修改数据库连接相关信息
sed -i "s|MYSQL_HOST|${MYSQL_HOST}|g" ${DEV_CONFIG}
sed -i "s|MYSQL_PORT|${MYSQL_PORT}|g" ${DEV_CONFIG}
sed -i "s|MYSQL_USER|${MYSQL_USER}|g" ${DEV_CONFIG}
sed -i "s|MYSQL_PASSWORD|${MYSQL_PASSWORD}|g" ${DEV_CONFIG}
sed -i "s|MYSQL_DB|${MYSQL_DB}|g" ${DEV_CONFIG}
sed -i "s|REDIS_HOST|${REDIS_HOST}|g" ${DEV_CONFIG}
sed -i "s|REDIS_PORT|${REDIS_PORT}|g" ${DEV_CONFIG}
sed -i "s|DJANGO_DEBUG|${DJANGO_DEBUG}|g" ${DEV_CONFIG}
if [[   ${REDIS_PASSWORD} != ""  ]]; then REDIS_PASSWORD=":${REDIS_PASSWORD}@"; fi
sed -i "s|:REDIS_PASSWORD@|${REDIS_PASSWORD}|g" ${DEV_CONFIG}
sed -i "s|REDIS_DB|${REDIS_DB}|g" ${DEV_CONFIG}
sed -i "s|ENV_LOCAL_TO_STREET_URL|${ENV_LOCAL_TO_STREET_URL}|g" ${DEV_CONFIG}
sed -i "s|ENV_ADDRESS_TO_LOCAL_URL|${ENV_ADDRESS_TO_LOCAL_URL}|g" ${DEV_CONFIG}
echo "修改数据库连接相关信息成功！"

echo "修改settings文件配置成功！"
ps -ef | grep ${PROJECT_PORT} |grep -v "grep"| awk '{print $2}' | xargs kill -9
echo "清理旧任务成功！"

${PYTHON_ENV}/uwsgi --http-socket ${PROJECT_HOST}:${PROJECT_PORT} --reload-on-rss 152 --harakiri 3600 -M  -p 8 -w "${PROJECT_NAME}.wsgi:application" --env PYTHONIOENCODING=utf-8 --static-map=/static=/home/renjing/django_auth_admin/static --daemonize $LOG_PATH
echo "执行任务成功！"


