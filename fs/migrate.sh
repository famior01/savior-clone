#!/bin/bash
cd /app/
/opt/venv/bin/python manage.py makemigrations
/opt/venv/bin/python manage.py makemigrations user
/opt/venv/bin/python manage.py migrate 
/opt/venv/bin/python manage.py migrate --run-syncdb 


