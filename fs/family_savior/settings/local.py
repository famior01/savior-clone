from .base import *
from decouple import config

SECRET_KEY = config('DJANGO_SECRET_KEY')
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

STATICFILES_DIRS = [
    BASE_DIR/"static",
    BASE_DIR/"profiles/static",
    BASE_DIR/"IWatch/static",
    # BASE_DIR/"user/static",
    BASE_DIR/"zakat_posts/static",
    # BASE_DIR/"authentications/static",
]

STATIC_ROOT = BASE_DIR/"staticfiles"

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR/'media'
# MEDIA_ROOT  = os.path.join(os.path.dirname(BASE_DIR), 'static_cdn', 'media_root')

