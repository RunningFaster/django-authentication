import datetime
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ohu=ohs#j@yrt#bwgcm4o#1#2q58s*q^t$&si@amwvbuevzue9'

DEBUG = True

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

    'organization',  # 组织架构
    'test_app',
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
# STATIC_ROOT =  os.path.join(BASE_DIR,'static')
STATICFILES_DIRS = [
    "./static/",
]
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/upload')

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
    'formatters': {
        'default': {
            'format': '%(asctime)s [%(levelname)s] [%(name)s:%(lineno)d]: %(message)s'
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
