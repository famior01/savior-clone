"""
WSGI config for family_savior project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import pathlib
from decouple import config

from django.core.wsgi import get_wsgi_application

# CURRENT_DIR = pathlib.Path(__file__).resolve().parent
# BASE_DIR = CURRENT_DIR.parent
# ENV_FILE_PATH = BASE_DIR / '.env'
# dotenv.read_dotenv(str(ENV_FILE_PATH))

production = config('USE_PRODUCTION', default=True, cast=bool)
testing = config('TESTING', cast=bool)

if production==True:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'family_savior.settings.production')
elif testing==True:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'family_savior.settings.testing')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'family_savior.settings.local')

application = get_wsgi_application()
