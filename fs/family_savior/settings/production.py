from .base import *
from decouple import config
import ssl


SECRET_KEY = config('DJANGO_SECRET_KEY')
DEBUG = False
ENV_ALLOWED_HOST = config('DJANGO_ALLOWED_HOSTS')
ALLOWED_HOSTS = ["137.184.250.152"]

# ====================================================
# ----------------- Email Settings -----------------
# ====================================================

# Reporting errors to admins
# ADMINS = [
#     ('Admin1', 'abuubaida901@gmail.com'),
# ]

# MANAGERS = ADMINS

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'filters': {
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse'
#         }
#     },
#     'formatters': {
#         'verbose': {
#             'format': '%(levelname)s %(asctime)s %(module)s '
#                     '%(process)d %(thread)d %(message)s'
#         },
#     },
#     'handlers': {
#         'mail_admins': {
#             'level': 'ERROR',
#             'filters': ['require_debug_false', ],
#             'class': 'django.utils.log.AdminEmailHandler'
#         },
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose',
#         },
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['mail_admins', ],
#             'level': 'ERROR',
#             'propagate': True
#         },
#         'django.security.DisallowedHost': {
#             'level': 'ERROR',
#             'handlers': ['console', 'mail_admins', ],
#             'propagate': True
#         }
#     }
# }


DEFAULT_FROM_EMAIL = config('EMAIL_USER')
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_SSL = True
EMAIL_PORT = 465
EMAIL_HOST_USER = config('EMAIL_USER') 
EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


    

# ======================================================================
# ------------------------- Postgres DATABASE SETTINGS -------------------
# ======================================================================
# https://www.enterprisedb.com/postgres-tutorials/how-use-postgresql-django

# DB_DATABASE=config('POSTGRES_DB')
# DB_USERNAME=config('POSTGRES_USER')
# DB_PASSWORD=config('POSTGRES_PASSWORD')
# DB_HOST=config('POSTGRES_HOST')
# DB_PORT=config('POSTGRES_PORT')

DB_HOST="savior-database-do-user-13416996-0.b.db.ondigitalocean.com"
DB_PORT="25060"
DB_PASSWORD="AVNS_81xAWmYcDGfRClcsV9l"
DB_USERNAME="doadmin"
DB_DATABASE="defaultdb"

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
    DATABASES['default']['OPTIONS'] = {
        'sslmode': 'require',
    }



# ===========================================================
# --------------------- CELERY SETTINGS ---------------------
# ===========================================================
# CELERY_BROKER_URL = config('CELERY_BROKER_REDIS_URL')
REDIS_HOST = config('DO_REDIS_URL', default='redis://localhost:6379/0')
CELERY_BROKER_URL = REDIS_HOST
# broker_use_ssl=True
# CELERY_RESULT_BACKEND = f'redis://{ENV_ALLOWED_HOST}:6379'
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

from ..cdn.conf import * # noqa




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