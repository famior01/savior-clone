#!/bin/bash
SUPERUSER_EMAIL = ${DJANGO_SUPERUSER_EMAIL:-'abuubaida901@gmail.com'}
SUPERUSER_USERNAME = ${DJANGO_SUPERUSER_USERNAME:-'admin'}
SUPERUSER_PASSWORD = ${DJANGO_SUPERUSER_PASSWORD:-'admin'}

cd /app/

/opt/venv/bin/python manage.py migrate --noinput
/opt/venv/bin/python manage.py createsuperuser --noinput --email $SUPERUSER_EMAIL --username $SUPERUSER_USERNAME  --password $SUPERUSER_PASSWORD  || true