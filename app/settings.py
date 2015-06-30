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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(PROJECT_ROOT, 'lib'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yh@juv9g%r!p#!l#)*$oukjw==5#!+j7e!f347700yk93k1ag^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'easy_thumbnails',
    'polymorphic',
    'ajaximage',
    'compressor',
    'endless_pagination',
    'ckeditor',
    'datetimewidget',

    'helper',
    'app.core',
    'app.account',
    'app.task',
    'app.comment',
    'app.route',
    'app.route.route1',
    'app.notification',
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
    'django.middleware.locale.LocaleMiddleware'
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
                'django.contrib.messages.context_processors.messages',
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

LANGUAGE_CODE = 'ru-ru'

# TIME_ZONE = 'Europe/Moscow'
USE_TZ = True

USE_I18N = True

USE_L10N = True

DATE_INPUT_FORMATS= ('%d.%m.%Y',)
DATE_FORMAT = 'd.m.Y'
FULL_DATE_FORMAT = 'd.m.Y'
# DATETIME_FORMAT = 'd.m.Y H:i' # чтобы заработало надо USE_L10N перевести в False
FULL_DATETIME_FORMAT = 'd.m.Y H:i'
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


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    # "constance.context_processors.config",
    "django.contrib.messages.context_processors.messages",
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

IMAGES_UPLOAD_FOLDER = 'images/'

AJAXIMAGE_AUTH_TEST = lambda u: True

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
# Copyscape
#
COPYSCAPE_USERNAME = 'bigt'
COPYSCAPE_API_KEY = 'ja05t7orfuo5w5hu'
# end Copyscape

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

from settings_custom import *
