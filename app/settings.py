# -*- coding: utf-8 -*-
"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

import os
import sys
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))
LOGS_FOLDER = os.path.join(PROJECT_DIR, os.pardir, 'logs')

sys.path.insert(0, os.path.join(PROJECT_ROOT, 'lib'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yh@juv9g%r!p#!l#)*$oukjw==5#!+j7e!f347700yk93k1ag^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 1

ADMINS = (
    ('volgoweb', 'volgoweb@bk.ru'),
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'fluent_comments',
    'crispy_forms',
    'django_comments',
    'django.contrib.sites',

    'easy_thumbnails',
    'polymorphic',
    'ajaximage',
    'compressor',
    'endless_pagination',
    'ckeditor',
    # 'datetimewidget',
    # 'tagging',
    # 'tagging_autosuggest',
    'mptt',
    'django_select2',
    # защита от подбора пароля
    'axes',
    # 'ajaxuploader',
    'ajax_upload',
    'timezones',
    'sitetree',
    'haystack',

    'helper',
    'app.core',
    'app.account',
    'app.task',
    'app.comment',
    'app.route',
    'app.route.route1',
    'app.notification',
    'app.wiki',
    'app.partner',
    'app.client',
    'app.contact',
    'app.crm',
    'app.goal',
    'app.idea',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'axes.middleware.FailedLoginMiddleware',
)

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                "django.core.context_processors.i18n",
                "django.core.context_processors.media",
                "django.core.context_processors.static",
                "django.core.context_processors.tz",
                'django.contrib.messages.context_processors.messages',
                'app.task.context_processors.task_counts',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Замена штатного пользователя на account
AUTH_USER_MODEL = 'account.Account'
AUTHENTICATION_BACKENDS = (
    'app.account.auth_backends.AccountModelBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'ru'
LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English'),
)

TIME_ZONE = 'Europe/Moscow'
USE_TZ = True

USE_I18N = True

USE_L10N = True

LOCALE_PATHS = (
    'locale',
)
DEFAULT_CHARSET = 'utf-8'

DATE_INPUT_FORMATS= ('%d.%m.%Y',)
DATE_FORMAT = 'd.m.Y'
# DATETIME_FORMAT = 'd.m.Y H:i' # чтобы заработало надо USE_L10N перевести в False
SHORT_DATE_FORMAT = 'd.m.Y'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static_all')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

MEDIA_ROOT = os.path.join(BASE_DIR, "files")
MEDIA_URL = '/files/'


# TEMPLATE_CONTEXT_PROCESSORS = (
#     "django.core.context_processors.request",
#     "django.contrib.auth.context_processors.auth",
#     "django.core.context_processors.debug",
#     "django.core.context_processors.i18n",
#     "django.core.context_processors.media",
#     "django.core.context_processors.static",
#     "django.core.context_processors.tz",
#     # "constance.context_processors.config",
#     "django.contrib.messages.context_processors.messages",
#     "app.task.context_processors.task_counts",
# )

# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
# )

IMAGES_UPLOAD_FOLDER = 'images/'

AJAXIMAGE_AUTH_TEST = lambda u: True


# EMAIL_USE_TLS = True
# EMAIL_HOST = 'imap.mail.ru'
# EMAIL_PORT = 993
# DEFAULT_FROM_EMAIL = 'work_together@server.service'
# EMAIL_HOST_USER = 'volgoweb@bk.ru'
# EMAIL_HOST_PASSWORD = ''


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_FOLDER, 'django.log'),
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
        'mail_to_adm':{
            'level':'INFO',
            'class':'django.utils.log.AdminEmailHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers':['console', 'logfile'],
            'propagate': True,
            'level':'DEBUG',
        },
        'django.request': {
            'handlers':['mail_to_adm', 'logfile'],
            'propagate': True,
            'level':'ERROR',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        '': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
    },
}

#
# fluent_comments
#
COMMENTS_APP = 'fluent_comments'
FLUENT_COMMENTS_EXCLUDE_FIELDS = ['name', 'email', 'url']
# end fluent_comments

#
# crispy_forms
#
CRISPY_TEMPLATE_PACK = 'bootstrap3'
# end crispy_forms

#
# Compressor:
#
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

COMPRESS_ROOT = os.path.join(PROJECT_DIR, "core", "static", "core", "less")
# COMPRESS_ROOT = os.path.join(PROJECT_DIR, "static_all", "core", "less")
COMPRESS_URL = STATIC_URL + 'core/less/'
COMPRESS_ENABLED = False
# end Compressor

#
# CKEditor
#
CKEDITOR_UPLOAD_PATH = os.path.join(MEDIA_ROOT, "ckeditor")
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        # 'toolbar': 'full',
        'width': '100%',
    },
    # 'full': {
    #     'width': '100%',
    #     'toolbar': 'full',
    # }
}
# end CKEditor

#
# AXES защита от подбора пароля
#
AXES_LOGIN_FAILURE_LIMIT = 10
AXES_COOLOFF_TIME = datetime.timedelta(minutes=5)
AXES_LOCKOUT_TEMPLATE = 'accounts/auth_temporally_lock.html'
# end AXES

#
# haystack работа с поисковыми движками
#
# Требуется определить в settings_custom.py
# HAYSTACK_CONNECTIONS = {
#     'default': {
#         'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
#         'URL': 'http://127.0.0.1:9200/',
#         'INDEX_NAME': 'haystack',
#     },
# }
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.BaseSignalProcessor'
ELASTICSEARCH_LOG = os.path.join(LOGS_FOLDER, 'es_trace.log')
# end haystack

from settings_custom import *
