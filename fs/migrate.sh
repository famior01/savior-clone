#!/bin/bash
SUPERUSER_EMAIL="abuubaida901@gmail.com"
SUPERUSER_FULLNAME="Abu-Ubaida"
SUPERUSER_RELIGION="Islam"
SUPERUSER_USERNAME="abuubaida01"
cd /app/

/opt/venv/bin/python3 manage.py makemigrations
/opt/venv/bin/python3 manage.py migrate 

/opt/venv/bin/python3 manage.py makemigrations user 
/opt/venv/bin/python3 manage.py migrate user

/opt/venv/bin/python3 manage.py makemigrations profiles 
/opt/venv/bin/python3 manage.py migrate profiles

/opt/venv/bin/python3 manage.py migrate --run-syncdb

/opt/venv/bin/python3 manage.py createsuperuser --email $SUPERUSER_EMAIL  --username $SUPERUSER_USERNAME --full_name $SUPERUSER_FULLNAME  --religion $SUPERUSER_RELIGION --noinput || true

# celery -A family_savior worker -l INFO -P eventlet

# /opt/venv/bin/celery -A family_savior worker -l INFO -P eventlet
/opt/venv/bin/celery -A family_savior worker -l INFO 

