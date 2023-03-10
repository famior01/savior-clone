#!/bin/bash

SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"abuubaida901@gmail.com"}
SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-"abuubaida01"}
SUPERUSER_FULLNAME=${DJANGO_SUPERUSER_FULLNAME:-"Abu-Ubaida"}
SUPERUSER_RELIGION=${DJANGO_SUPERUSER_RELIGION:-"Islam"}
SUPERUSER_GENDER=${DJANGO_SUPERUSER_GENDER:-"Male"}
SUPERUSER_DOB=${DJANGO_SUPERUSER_DOB:-"2001-09-21"}

cd /app/

/opt/venv/bin/python manage.py createsuperuser --email $SUPERUSER_EMAIL --username $SUPERUSER_USERNAME --full_name $SUPERUSER_FULLNAME --religion $SUPERUSER_RELIGION --gender $SUPERUSER_GENDER --date_of_birth $SUPERUSER_DOB --noinput  || true
