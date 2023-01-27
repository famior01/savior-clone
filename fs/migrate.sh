#!/bin/bash

SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"abuubaida901@gmail.com"}
SUPERUSER_FULLNAME=${DJANGO_SUPERUSER_FULLNAME:-"Abu-Ubaida"}
SUPERUSER_RELIGION=${DJANGO_SUPERUSER_RELIGION:-"Islam"}
SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-"abuubaida01"}

cd /app/

/opt/venv/bin/python manage.py migrate sites --noinput
/opt/venv/bin/python manage.py migrate --noinput
/opt/venv/bin/python manage.py runsyncdb --noinput
/opt/venv/bin/python manage.py createsuperuser --email $SUPERUSER_EMAIL  --username $SUPERUSER_USERNAME --full_name $SUPERUSER_FULLNAME  --religion $SUPERUSER_RELIGION --noinput || true
