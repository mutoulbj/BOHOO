#encoding=utf-8
import os
ROOT_PATH = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
# ('Your Name', 'your_email@example.com'),
)

SITE_ID = 1

AUTH_USER_MODEL = 'User.MyUser'

ACCOUNT_ACTIVATION_DAYS = 7
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = '@qq.com'
EMAIL_HOST_PASSOWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = '@qq.com'

LOGIN_URL = '/accounts/login'

# 分页
PAGINATION_PER_PAGE = 2


AUTHENTICATION_BACKENDS = ('Bohoo.backends.EmailAuthBackend', 'django.contrib.auth.backends.ModelBackend',)


DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
       'NAME': 'groupv3',                      # Or path to database file if using sqlite3.
       'USER': 'root',                      # Not used with sqlite3.
       'PASSWORD': '1234',                  # Not used with sqlite3.
       'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
       'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
   }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh_CN'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
# MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media').replace("\\", '/')
MEDIA_ROOT = '/home/fan/media/'
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ROOT_PATH + '/static'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# django-avatar 设置
AVATAR_STORAGE_DIR = 'avatars/'
# AVATAR_STORAGE = MEDIA_ROOT

# group_avatar 设置,基本与django-avatar相同,在`avatar`前加`group`前缀,`AVATAR`前加`GROUP`前缀,下划线连接
GROUP_AVATAR_STORAGE_DIR = 'group_avatars/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), '../static').replace("\\", '/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'c4n%_0ool&amp;2k*^#tik%8ihi)l#51w9$ciqu()whp4s4e3#j_oh'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)
ROOT_URLCONF = 'Bohoo.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'Bohoo.wsgi.application'

DIRNAME = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(DIRNAME, 'templates').replace("\\", '/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'bootstrap_toolkit',
    'compressor',
    'avatar',
    'group_avatar',
    'captcha',  # 验证码app
    'django.contrib.admin',
    'User',
    'groups',
    'accounts',
    'friends',
    'django_messages',
    'social',
    'sys_notification'
    # 'notification',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#SITE = 'http://127.0.0.1:8000' if DEBUG else 'http://qinxuye.me'
SITE = 'http://127.0.0.1:8000'

ENABLE_GOOGLE_ACCOUNT = False
GOOGLE_API = {
    'client_id': '',
    'client_secret': '',
    'redirect_urls': '',
    'refresh_token': '',
}
GOOGLE_AUTH_ENDPOINT = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_ACCESS_TOKEN_ENDPOINT = 'https://accounts.google.com/o/oauth2/token'
GOOGLE_USERINFO_ENDPOINT = 'https://www.googleapis.com/oauth2/v1/userinfo'
GOOGLE_REDIRECT_URI = '%s/accounts/google/login/done/' % SITE

# Weibo
ENABLE_WEIBO_ACCOUNT = False
WEIBO_API = {
    'app_key': '1387478159',
    'app_secret': '44cb8e49ef1e8260a8215c5e82c006b4',
    'redirect_urls': '/',
}
WEIBO_AUTH_ENDPOINT = 'https://api.weibo.com/oauth2/authorize'
WEIBO_ACCESS_TOKEN_ENDPOINT = 'https://api.weibo.com/oauth2/access_token'
WEIBO_REDIRECT_URI = '%s/accounts/weibo/login/done/' % SITE
WEIBO_OAUTH_VERSION = 2
WEIBO_API_ENDPOINT = 'https://api.weibo.com/%d/' % WEIBO_OAUTH_VERSION

# Renren
ENABLE_RENREN_ACCOUNT = False
RENREN_API = {
    'api_key': '',
    'secret_key': '',
    'redirect_urls': '',
    'refresh_token': '' # use to sync data when a post is created or else
}
RENREN_AUTH_ENDPOINT = 'https://graph.renren.com/oauth/authorize'
RENREN_ACCESS_TOKEN_ENDPOINT = 'https://graph.renren.com/oauth/token'
RENREN_REDIRECT_URI = '%s/accounts/renren/login/done/' % SITE
RENREN_API_ENDPOINT = 'http://api.renren.com/restserver.do'

# QQWeibo
ENABLE_QQWEIBO_ACCOUNT = False
QQWEIBO_API = {
    'app_key': '',
    'app_secret': '',
    'redirect_urls': '',
    'access_token_key': '', # use for oauth1 to sync data when a post is created or else
    'access_token_secret': '' # use for oauth1 to sync data when a post is created or else
}
QQWEIBO_REDIRECT_URI = '%s/accounts/qqweibo/login/done/' % SITE




TOPIC_IMAGE_PATH = "/home/fan/media/topic_image/"

HASH_KEY = 'p0o9i8u7y6t5r4e3w2q1'

try:
    from settings_dev import *
except ImportError:
    pass
