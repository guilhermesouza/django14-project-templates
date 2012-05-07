#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    PROJECT_NAME = '{{ project_name }}'
    PROJECT_ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

    sys.path.append(os.path.join(PROJECT_ROOT_PATH, PROJECT_NAME))
    sys.path.append(os.path.join(PROJECT_ROOT_PATH, PROJECT_NAME, 'apps'))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
            "%s.settings" % PROJECT_NAME)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
