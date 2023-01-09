from pathlib import Path
import os
import smtplib, ssl


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9x5e3shen*+a66vk360$0ncpk^4+!o4(mps)e_6tmih(smob^e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allowed hosts for the project to run on 
ALLOWED_HOSTS = []

# LOGIN_URL ='/admin/'
# Here If User logged in then he will be redirected to this page

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_celery_results',
    'django_celery_beat',
    'rest_framework',
    'user',
    'profiles',
    'posts',
    'zakat_posts',
    'AI',

    # django-allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'authentications', 

    # for notifications
    'notifications',
    'crispy_forms',

    # phone number field
    "phonenumber_field",
]

AUTH_USER_MODEL = 'user.User'

# ---------------------------------------------------------------------------- #
#                              PHONE NUMBER FORMAT                             #
# ---------------------------------------------------------------------------- #
# https://django-phonenumber-field.readthedocs.io/en/latest/
PHONENUMBER_DEFAULT_FORMAT = 'INTERNATIONAL'
PHONENUMBER_DB_FORMAT = 'E164'
PHONENUMBER_DEFAULT_REGION = "PK"


# ---------------------------------------------------------------------------- #
#                               Allauth settings                               #
# ---------------------------------------------------------------------------- #

# https://django-allauth.readthedocs.io/en/latest/configuration.html 

SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_FULL_NAME_REQUIRED = True
ACCOUNT_RELIGION_REQUIRED = True
ACCOUNT_PHONE_NUMBER_REQUIRED = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_NAME_REQUIRED = True
# ACCOUNT_FIRST_NAME_REQUIRED = True
# ACCOUNT_LAST_NAME_REQUIRED = True
LOGIN_REDIRECT_URL = '/zakat_posts/'
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_EMAIL_CONFIRMATION_HMAC = True

ACCOUNT_FORMS = {
'signup': 'authentications.forms.CustomSignupForm',
}

# ---------------------------------------------------------------------------- #
#                                Email settings                                #
# ---------------------------------------------------------------------------- #
# ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
# # to show the subject of the email
# ACCOUNT_EMAIL_SUBJECT_PREFIX = "Assalam O Alaikum 👋 \n"
# after these second, user can request of email confirmation 
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 180
# user can change his email address 3 times only!
ACCOUNT_MAX_EMAIL_ADDRESSES = 1 
# user failed attempts to login are limited to 5
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 4
# after these second, user can try to login again
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 180
# user cannot loged in after varification, he will redirect to annonymous url
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
# Remember me is enabled by default
ACCOUNT_SESSION_REMEMBER = True
# limit of alphanumeric characters in username
ACCOUNT_USERNAME_MIN_LENGTH = 5

# instead of website@gmail.com, now it will be abuubaida901@gmail.com
DEFAULT_FROM_EMAIL = 'famior01@gmail.com'


# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_USE_TLS = True
EMAIL_USE_SSL = True
EMAIL_PORT = 465
# we will provide our email and password in the .env file
EMAIL_HOST_USER = 'famior01@gmail.com'
EMAIL_HOST_PASSWORD = 'ddkbuimnyedhkmpy'


# ===========================================================
# ------------------------- DEFAULT SETTINGS ------------------
# ===========================================================
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'family_savior.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                # `allauth` needs this from django
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # Enable {{ STATIC_URL }} and {{ MEDIA_URL }}
                'django.template.context_processors.media',
                'django.template.context_processors.static',

                # Enable {{ profile_picture }}
                'profiles.context_processors.profile_picture',

            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

]

WSGI_APPLICATION = 'family_savior.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Cashe
# django setting.
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#         'LOCATION': 'my_cache_table',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Karachi'

USE_I18N = True

USE_TZ = True

# ===========================================================
# --------------------- CELERY SETTINGS ---------------------
# ===========================================================
# Celery settings
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
# if i want to use redis as a result backend, but i am using django database
# CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Karachi'
CELERY_RESULT_BACKEND = 'django-db'
# CELERY_CACHE_BACKEND = 'django-cache'
CELERY_CACHE_BACKEND = 'default'
# CELERY_BEAT
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
RESULT_BACKEND = 'db+sqlite:///results.db'




#=================================================
# ------------- STATIC FILES ---------------------
# =================================================
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    BASE_DIR/'posts'/'static',
    BASE_DIR/'profiles'/'static',
    BASE_DIR/'zakat_posts'/'static',
    BASE_DIR/'authentications'/'static',
]

# Media files (User uploaded files)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR/'media'
# MEDIA_ROOT  = os.path.join(os.path.dirname(BASE_DIR), 'static_cdn', 'media_root')





# =====================================================
# ------------------- DATABASE ------------------------
# =====================================================
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




# =====================================================
# ------------------- Notifications -------------------
# =====================================================
# docs = https://github.com/django-notifications/django-notifications

DJANGO_NOTIFICATIONS_CONFIG = { 'USE_JSONFIELD': True}
DJANGO_NOTIFICATIONS_CONFIG = { 'SOFT_DELETE': True}