from os.path import dirname, realpath
project_path = realpath(dirname(__file__))

from sys import path
path.append(project_path)

from os import environ
#environ['PYTHON_EGG_CACHE'] = '/home/sysproject/data/django/.python-eggs'
environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.handlers import wsgi
application = wsgi.WSGIHandler()