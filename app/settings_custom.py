# -*- coding: utf-8 -*-
from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wt',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'TEST': {
            'NAME': 'wt_test',
        },
        'OPTIONS': {
           "init_command": "SET storage_engine=MyISAM",
        },
    },
}


#
# PuDB отладка
#
MIDDLEWARE_CLASSES += ('django_pdb.middleware.PdbMiddleware',)
#DEBUG_PROPAGATE_EXCEPTIONS = True
INSTALLED_APPS += ('django_pdb',)

#
# haystack работа с поисковыми движками
#
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://192.168.1.37:9200/',
        'INDEX_NAME': 'test_dk',
    },
}
# end haystack


# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.mail.ru'
# EMAIL_PORT = 587
# DEFAULT_FROM_EMAIL = 'info@smk.local'
# EMAIL_HOST_USER = 'dima_page@mail.ru'
# EMAIL_HOST_PASSWORD = 'lbvf-vskj'
