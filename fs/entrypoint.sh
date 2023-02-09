#!/bin/bash
APP_PORT=${PORT}
HOST=${DJANGO_ALLOWED_HOSTS:-"104.248.98.131"}
cd /app/
/opt/venv/bin/gunicorn --workers=1  --worker-class=gthread family_savior.wsgi:application --bind "${HOST}:${APP_PORT}"
