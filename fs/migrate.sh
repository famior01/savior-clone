#!/bin/bash
cd /app/

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate 
python manage.py migrate --run-syncdb

celery -A family_savior worker -l INFO 

