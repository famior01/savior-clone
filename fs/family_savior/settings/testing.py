from .base import *
from decouple import config
import ssl
import os 

SECRET_KEY ="alsdjflk;dslkdsfjsdljldsjflkjdsfjsdfj;dslkjfsdhfljdshf"
DEBUG =False
ALLOWED_HOSTS=['*']

# ====================================================
# ----------------- Email Settings -----------------
# ====================================================
DEFAULT_FROM_EMAIL=os.environ.get('EMAIL_USER')
EMAIL_HOST ='smtp.gmail.com' 
EMAIL_USE_SSL =True
EMAIL_PORT =465
EMAIL_HOST_USER =os.environ.get('EMAIL_USER') 
EMAIL_HOST_PASSWORD =os.environ.get('EMAIL_PASSWORD')
EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'


# ======================================================================
# ------------------------- Postgres DATABASE SETTINGS -------------------
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
# CELERY_BROKER_URL = config('CELERY_BROKER_REDIS_URL')
REDIS_HOST ='redis://localhost:6379'
CELERY_BROKER_URL =REDIS_HOST
BROKER_USE_SSL = {'ssl_cert_reqs': ssl.CERT_REQUIRED,}
CELERY_RESULT_BACKEND = REDIS_HOST
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 7200} # 2 hours
CELERY_ACCEPT_CONTENT =['application/json']
CELERY_TASK_SERIALIZER ='json'
CELERY_RESULT_SERIALIZER ='json'
CELERY_TIMEZONE ='Asia/Karachi'
CELERY_RESULT_BACKEND ='django-db'
# CELERY_CACHE_BACKEND = 'django-cache'
CELERY_CACHE_BACKEND ='default'
CELERY_BEAT_SCHEDULER ='django_celery_beat.schedulers:DatabaseScheduler'
RESULT_BACKEND ='db+sqlite://results.db'


# =====================================================================
# ------------------------- Django Ignor some 404 errors -------------------
# =====================================================================
import re
IGNORABLE_404_URLS = [
    re.compile(r'\.(php|cgi)$'),
    re.compile(r'^/phpmyadmin/'),
]


#=================================================
# ------------- STATIC FILES ---------------------
# =================================================
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR/"staticfiles"

# STATICFILES_DIRS = [
#     BASE_DIR / "staticfiles"
# ]
# python manage.py collectstatic --noinput  # to collect static files

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR/'media'
# it overrides static_root
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
# -------------------   extra loggers  -----------------------
# =====================================================
# 'django.security.DisallowedHost': {
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