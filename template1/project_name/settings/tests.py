# -*- coding: utf8 -*-

import os
from settings.defaults import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
LOCAL = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT_PATH, 'test.sqlite3'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

MEDIA_ROOT = os.path.join(PROJECT_ROOT_PATH, 'media_tests')

INSTALLED_APPS += ('django_coverage', )

# Coverage settings
from django_coverage.settings import *

COVERAGE_MODULE_EXCLUDES += [
    # packages
    'south',

    # modules
    'admin',
    'feeds',
    'fixtures',
    'managers',
    'sitemaps',
]
