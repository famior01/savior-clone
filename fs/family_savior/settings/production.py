from .base import *


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

DEBUG = False

ENV_ALLOWED_HOST = os.environ.get('DJANGO_ALLOWED_HOSTS')
ALLOWED_HOSTS = [ ENV_ALLOWED_HOST ]


# ====================================================
# ----------------- Email Settings -----------------
# ====================================================
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_USER')
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_SSL = True
EMAIL_PORT = 465
EMAIL_HOST_USER = os.environ.get('EMAIL_USER') 
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'




# ======================================================================
# ------------------------- Postgres DATABASE SETTINGS -------------------
# ======================================================================
# https://www.enterprisedb.com/postgres-tutorials/how-use-postgresql-django
DB_IGNORE_SSL=os.environ.get('DB_IGNORE_SSL')=='true'

POSTGRES_READY=os.environ.get('POSTGRES_READY', False)
DB_DATABASE=os.environ.get('POSTGRES_DB')
DB_USERNAME=os.environ.get('POSTGRES_USER')
DB_PASSWORD=os.environ.get('POSTGRES_PASSWORD')
DB_HOST=os.environ.get('POSTGRES_HOST')
DB_PORT=os.environ.get('POSTGRES_PORT')

DB_IS_AVAILABLE = all([
    DB_DATABASE, DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT 
])


if DB_IS_AVAILABLE:
    DATABASES = {
        'default': {
            "ENGINE": "django.db.backends.postgresql",
            'NAME': DB_DATABASE,
            'USER': DB_USERNAME,
            'PASSWORD': DB_PASSWORD,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
        }
    }
    if not DB_IGNORE_SSL:
        DATABASES['default']['OPTIONS'] = {
            'sslmode': 'require',
        }



# ===========================================================
# --------------------- CELERY SETTINGS ---------------------
# ===========================================================
# CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_REDIS_URL')
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
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


#=================================================
# ------------- STATIC FILES ---------------------
# =================================================
STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR/"staticfiles-cdn"

STATICFILES_DIRS = [
    BASE_DIR/"staticfiles"
]

from .cdn.conf import * # noqa




# =====================================================
# ------------------- HTTPS SETTINGS -------------------------
# =====================================================
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_BROWSER_XSS_FILTER = True
# X_FRAME_OPTIONS = 'DENY'

# =====================================================
# -------------------   HSTS SETTINGS-------------------------
# =====================================================

# SECURE_HSTS_SECONDS = 31536000 # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True # include all subdomains
# SECURE_HSTS_PRELOAD = True # preload HSTS on browser start