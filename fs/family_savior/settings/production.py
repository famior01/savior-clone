from .base import *
from decouple import config
import ssl
import os 

SECRET_KEY=config('DJANGO_SECRET_KEY')
DEBUG=False
ENV_ALLOWED_HOST=config('DJANGO_ALLOWED_HOSTS')
DOMAIN_NAME=config('DOMAIN_NAME')
# ALLOWED_HOSTS=[ "34.131.57.36", DOMAIN_NAME, 'savior.website']
ALLOWED_HOSTS=["10.72.0.10","10.72.0.11","savior.website", DOMAIN_NAME, "10.76.13.100", "34.131.57.36", "34.117.175.183"]    
# ====================================================
# ----------------- Email Settings -----------------
# ====================================================
DEFAULT_FROM_EMAIL=config('EMAIL_USER')
EMAIL_HOST ='smtp.gmail.com' 
EMAIL_USE_SSL =True
EMAIL_PORT =465
EMAIL_HOST_USER =config('EMAIL_USER') 
EMAIL_HOST_PASSWORD =config('EMAIL_PASSWORD')
EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'


# ======================================================================
# ------------------------- Postgres DATABASE SETTINGS -------------------
# ======================================================================
# https://www.enterprisedb.com/postgres-tutorials/how-use-postgresql-django
DB_USERNAME=config('DB_USERNAME')
DB_PASSWORD=config('DB_PASSWORD')
DB_HOST= "/cloudsql/high-function-378716:asia-south2:saviordb"
DB_PORT=config('DB_PORT')  
DB_DATABASE=config('DB_NAME')  

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
REDIS_HOST =config('DO_REDIS_URL')
CELERY_BROKER_URL =REDIS_HOST 
CELERY_BROKER_URL = 'redis://localhost:6379'
BROKER_USE_SSL = {'ssl_cert_reqs': ssl.CERT_REQUIRED,}
# CELERY_RESULT_BACKEND = REDIS_HOST
# BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 7200} # 2 hours
CELERY_ACCEPT_CONTENT =['application/json']
CELERY_TASK_SERIALIZER ='json'
CELERY_RESULT_SERIALIZER ='json'
CELERY_TIMEZONE ='Asia/Karachi'
CELERY_RESULT_BACKEND ='django-db'
# CELERY_CACHE_BACKEND = 'django-cache' 
CELERY_CACHE_BACKEND ='default'
CELERY_BEAT_SCHEDULER ='django_celery_beat.schedulers:DatabaseScheduler'
# RESULT_BACKEND ='db+sqlite://results.db'



# =================================================
# ------------- CSRF_TRUSTED_ORIGINS ---------------------
# =================================================
CSRF_TRUSTED_ORIGINS=['https://savior.website','https://*.savior.website','https://www.savior.website']

#=================================================
# ------------- STATIC FILES ---------------------
# =================================================
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "staticfiles-cdn",
]

# from ..cdn.conf import * # noqa1 

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



# =====================================================
# -------------------   LOGGERS -----------------------
# =====================================================
ADMINS = [
    ('Admin1', 'abuubaida901@gmail.com'),
    ('Admin2', 'saviore01@gmail.com'),
    ('Admin3', 'famior01@gmail.com'),
]
MANAGERS = ADMINS

FORMATTERS = (
    {
        "console": {
            "format": "{levelname} {asctime:s} {name} {module} {filename} {lineno:d} {funcName} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {asctime:s} {name} {module} {filename} {lineno:d} {funcName} {message}",
            "style": "{",
        },
    },
)

HANDLERS = {
    'mail_admins': {
        'level': 'ERROR',
        'class': 'django.utils.log.AdminEmailHandler',
        'formatter': 'simple',
    },
    'console': {
        'level': 'DEBUG',
        'class': 'logging.StreamHandler',
        'formatter': 'console',
    },
}

LOGGERS = {
    'django.request': {
        'handlers': ['mail_admins', ],
        'level': 'ERROR',
        'propagate': True
    },
    'django.security.DisallowedHost': {
        'level': 'INFO',
        'handlers':[ 'console' ,'mail_admins', ],
        'propagate': True
    },
    'django.db.backends': {
        'level': 'INFO',
        'handlers':[ 'console' ,'mail_admins', ],
        'propagate': True
    },
    'django.security.SuspiciousOperation': {
        'level': 'INFO',
        'handlers': [ 'console' ,'mail_admins', ],
        'propagate': True
    },
    'django.server': {
        'level': 'INFO',
        'handlers': [ 'console' ,'mail_admins', ],
        'propagate': True
    },  
    'django.security': {
        'level': 'INFO',
        'handlers': ['console' ,'mail_admins', ],
        'propagate': True
    },
    'django.template': {
        'level': 'INFO',
        'handlers': ['console' ,'mail_admins', ],
        'propagate': True
    },
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    "formatters": FORMATTERS[0],
    "handlers": HANDLERS,
    "loggers": LOGGERS,
}



# =====================================================
# -------------------   AWS SETTINGS -----------------------
# =====================================================
#  'django.security': {
#         'level': 'INFO',
#         'handlers': ['console' ,'mail_admins', ],
#         'propagate': True
#     },
#     'django.template': {
#         'level': 'INFO',
#         'handlers': ['console' ,'mail_admins', ],
#         'propagate': True
#     },
#     'django.security.DisallowedHost': {
#         'level': 'INFO',
#         'handlers': ['mail_admins', ],
#         'propagate': True
#     },
#     'django.db.backends': {
#         'level': 'INFO',
#         'handlers': ['mail_admins', ],
#         'propagate': True
#     },
#     'django.security.SuspiciousOperation': {
#         'level': 'INFO',
#         'handlers': ['mail_admins', ],
#         'propagate': True
#     },
#     'django.server': {
#         'level': 'INFO',
#         'handlers': [ 'console' ,'mail_admins', ],
#         'propagate': True
#     },