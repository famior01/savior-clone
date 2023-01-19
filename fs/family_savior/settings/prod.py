from .base import *
import os

with open(os.path.join(BASE_DIR, 'secret_key.txt')) as f:
    SECRET_KEY = f.read().strip()
# SECRET_KEY = os.environ.get('SECRET_KEY')
# SECRET_KEY = 'ox5pd#^_zj!enw81&-b6^amb2ik#rx+a0ebv6wt&*$&fwlrqv9'

DEBUG = True

ALLOWED_HOSTS = ['128.199.29.110']

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myproject',
        'USER': 'abuubaida01',
        'PASSWORD': 'Fd1|@Fn2|7*dn',
        'HOST': '128.199.29.110',
        'PORT': '',
    }
}
