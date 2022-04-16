import os

from .base import *

# Security

DEBUG = False

ALLOWED_HOSTS = ['dndmap.frankanema.nl']

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True


# Rest

PYTHON_EXECUTABLE = '~/venv-dndmap/bin/python'
