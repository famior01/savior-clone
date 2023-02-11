#!/bin/bash
cd /app/
SUPERUSER_EMAIL="abuubaida901@gmail.com"
SUPERUSER_FULLNAME="Abu-Ubaida"
SUPERUSER_RELIGION="Islam"
SUPERUSER_USERNAME="abuubaida01"
SUPERUSER_PASSWORD="Fs1|@Fr2|7*"

/opt/venv/bin/python manage.py createsuperuser --email $SUPERUSER_EMAIL  --username $SUPERUSER_USERNAME --full_name $SUPERUSER_FULLNAME  --religion $SUPERUSER_RELIGION --password $SUPERUSER_PASSWORD --noinput || true
