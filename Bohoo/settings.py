#encoding=utf-8
import os
ROOT_PATH = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
# ('Your Name', 'your_email@example.com'),
)

SITE_ID = 1
MANAGERS = ADMINS

AUTH_USER_MODEL = 'User.MyUser'

ACCOUNT_ACTIVATION_DAYS = 7
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = '@qq.com'
EMAIL_HOST_PASSOWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = '@qq.com'

LOGIN_URL = '/accounts/login'

ENDLESS_PAGINATION_PER_PAGE = 50

ENDLESS_PAGINATION_NEXT_LABEL = "Next"
ENDLESS_PAGINATION_DEFAULT_CALLABLE_AROUNDS = 5
ENDLESS_PAGINATION_DEFAULT_CALLABLE_ARROWS = True
ENDLESS_PAGINATION_FIRST_LABEL = "First"
ENDLESS_PAGINATION_LAST_LABEL = "Last"

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

# django-avatar 设定
AVATAR_STORAGE_DIR = 'avatars/'
# AVATAR_STORAGE = MEDIA_ROOT

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
    'compressor',
    'avatar',
    'django.contrib.admin',
    'User',
    'groups',
    'accounts',
    'endless_pagination',
    'friends',
    'django_messages',
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
