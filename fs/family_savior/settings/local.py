from .base import *
from decouple import config
import os

SECRET_KEY = "ox5pd@^_zj!enw81&-b6&34mb2ik@rx+a0ebv6wt&324&fwlrqv9"
DEBUG = True
ALLOWED_HOSTS = []


# ====================================================
# ----------------- Email Settings -----------------
# ====================================================
DEFAULT_FROM_EMAIL = config('EMAIL_USER')
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_SSL = True
EMAIL_PORT = 465
EMAIL_HOST_USER = config('EMAIL_USER') 
EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD')
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'




# ======================================================================
# ------------------------- Sqlit3 DATABASE SETTINGS -------------------
# ======================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ===========================================================
# --------------------- CELERY SETTINGS ---------------------
# ===========================================================
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
BROKER_USE_SSL = {'ssl_cert_reqs': ssl.CERT_REQUIRED,}
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 7200} # 2 hours
CELERY_RESULT_BACKEND = "django-db"
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Karachi'
CELERY_RESULT_BACKEND = 'django-db'
# CELERY_CACHE_BACKEND = 'django-cache'
CELERY_CACHE_BACKEND = 'default'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
RESULT_BACKEND = 'db+sqlite://results.db'


# ===========================================================
# --------------------- STATIC FILES SETTINGS ---------------------
# ===========================================================

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR/"staticfiles"

# python manage.py collectstatic --noinput  # to collect static files

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR/'media'