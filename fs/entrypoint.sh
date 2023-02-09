#!/bin/bash
APP_PORT=${PORT}
HOST=${DJANGO_ALLOWED_HOSTS}
cd /app/
/opt/venv/bin/gunicorn --workers=1  --worker-class=gthread family_savior.wsgi:application --bind "${HOST}:${APP_PORT}"
