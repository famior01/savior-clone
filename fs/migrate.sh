#!/bin/bash
cd /app/

/opt/venv/bin/python manage.py makemigrations
/opt/venv/bin/python manage.py migrate --noinput
/opt/venv/bin/python manage.py migrate --run-syncdb --noinput

/opt/venv/bin/celery -A family_savior worker -l INFO 


