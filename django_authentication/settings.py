import datetime
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ohu=ohs#j@yrt#bwgcm4o#1#2q58s*q^t$&si@amwvbuevzue9'

from config import *

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'debug_toolbar',  # 调试信息
    'rest_framework',  # drf
    'corsheaders',  # 跨域方案
    'djcelery',  # 异步

    'organization',  # 组织架构
]

INTERNAL_IPS = ['127.0.0.1']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # 跨域问题解决方案
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # 调试界面
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_authentication.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_authentication.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 设置时区
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False
DATETIME_FORMAT = "Y年n月j日 H:i:s"

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    "./static/",
]
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
# 文件存储配置
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # 默认根目录

REST_FRAMEWORK = {
    # 处理对象时间格式
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    # 自定义分页工具
    'DEFAULT_PAGINATION_CLASS': 'basic.page_pagination.PaginationResponse',
    'PAGE_SIZE': 10,
    # 新版drf schema_class默认用的是rest_framework.schemas.openapi.AutoSchema
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    # 允许的请求数据格式
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    # 允许的返回数据格式
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    # # 自定义认证
    # 'DEFAULT_AUTHENTICATION_CLASSES': [
    #     'basic.base_authorization.JWTAuthentication',
    # ],
    # # 自定义权限
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'basic.base_authorization.AdminPermission',
    # ],
    # 自定义异常信息处理
    'EXCEPTION_HANDLER': 'basic.base_exception.common_exception_handler'
}

JWT_AUTH = {
    'JWT_AUTH_HEADER_PREFIX': 'JWT',  # 设置 请求头中的前缀
    # 自定义用户生成token时使用的secret信息，作用于如果用户进行密码修改，则原token在进行验证时则会失败
    # 'JWT_GET_USER_SECRET_KEY': 'users.utils.jwt_get_user_secret',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=100000),
}

# 日志信息
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': PROJECT_LOG_PAHT + 'jingan_recyclable.log',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'default',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'db_console': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': PROJECT_LOG_PAHT + 'jingan_recyclable_db.log',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'db.backends',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
        },
        'django.db.backends': {
            'handlers': ['db_console'],
            'propagate': True,
            'level': 'DEBUG',
        },
    },
    'formatters': {
        'default': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]-\n%(message)s'
        },
        'db.backends': {
            'format': '%(message)s'
        }
    },
}

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
)

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': MYSQL_DB,
        'USER': MYSQL_USER,
        'PASSWORD': MYSQL_PASSWORD,
        'HOST': MYSQL_HOST,
        'PORT': MYSQL_PORT,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

#############################
# celery 配置信息 start
#############################
import djcelery

djcelery.setup_loader()
RABBITMQ_CONFIG = "pyamqp://guest_test:guest@118.25.75.75:5673/DjangoAuth"
BROKER_URL = RABBITMQ_CONFIG
# 消息代理
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
# 并发worker数
CELERYD_CONCURRENCY = 4
# 每个worker最多执行完100个任务就会被销毁，可防止内存泄露
CELERYD_MAX_TASKS_PER_CHILD = 10
# 任务发出后，经过一段时间还未收到acknowledge , 就将任务重新交给其他worker执行
CELERY_DISABLE_RATE_LIMITS = True
# 防止死锁
CELERYD_FORCE_EXECV = True
# 通用格式
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
#############################
# celery 配置信息 end
#############################

# 定时任务
CELERYBEAT_SCHEDULE = {
    'test_app.tasks.verify': {
        "task": "test_app.tasks.verify",
        "schedule": datetime.timedelta(seconds=5),  # 每5秒执行一下receive_mail函数
        "args": (),  # 参数
    }
}
