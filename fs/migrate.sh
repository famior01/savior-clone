#!/bin/bash
cd /app/

# /opt/venv/bin/pip install -r requirements.txt
/opt/venv/bin/python manage.py makemigrations user
/opt/venv/bin/python manage.py migrate 
/opt/venv/bin/python manage.py migrate --run-syncdb 

# /opt/venv/bin/celery -A family_savior worker -l INFO 


