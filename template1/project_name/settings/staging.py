# -*- coding: utf8 -*-

from settings.defaults import *

STATIC_ROOT = '/home/{{ project_name }}_static'
MEDIA_ROOT = '/home/{{ project_name }}_media'

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': '{{ project_name }}_db',
    'USER': 'root',
    'PASSWORD': '',
    'HOST': 'localhost',
    'PORT': '',
}
