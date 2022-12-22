"""
WSGI config for mensajeriaapp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mensajeriaapp.settings')

application = get_wsgi_application()

import importlib
if __name__ == '__main__':
    print("In main.py")
    package = importlib.import_module('hello', package='./')
    print("Loaded hello.py")
    package.hello()