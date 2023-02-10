#!/bin/bash
cd /app/

pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate 
python3 manage.py migrate --run-syncdb

celery -A family_savior worker -l INFO 

