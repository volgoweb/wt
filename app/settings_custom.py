

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wt',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'OPTIONS': {
           "init_command": "SET storage_engine=MyISAM",
        },
    }
}


# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.mail.ru'
# EMAIL_PORT = 587
# DEFAULT_FROM_EMAIL = 'info@smk.local'
# EMAIL_HOST_USER = 'dima_page@mail.ru'
# EMAIL_HOST_PASSWORD = 'lbvf-vskj'
