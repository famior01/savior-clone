from .base import *
import os

with open(os.path.join(BASE_DIR, 'secret_key.txt')) as f:
    SECRET_KEY = f.read().strip()

DEBUG = True

ALLOWED_HOSTS = ['52.66.205.18']


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
