"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv
project_folder = os.path.expanduser("~/NgStore2")
load_dotenv(os.path.join(project_folder, ".env"))
import sys

path = "/home/Pycobra/NgStore2"
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'NgStore2.settings.core_settings'
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NgStore2.settings.core_settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
app=application