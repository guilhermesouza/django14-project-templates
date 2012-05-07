import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append(('/'.join(os.path
    .abspath(os.path.dirname(__file__)).split('/')[:-2])))

os.environ['DJANGO_SETTINGS_MODULE'] = '{{ project_name }}.settings.staging'
application = get_wsgi_application()
