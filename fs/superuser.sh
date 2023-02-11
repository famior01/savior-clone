#!/bin/bash
SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"abuubaida901@gmail.com"}
cd /app/

/opt/venv/bin/python manage.py createsuperuser --email $SUPERUSER_EMAIL --noinput || true