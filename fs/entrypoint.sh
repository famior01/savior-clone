#!/bin/bash
APP_PORT=${PORT:-8000}
cd /app/
/opt/venv/bin/gunicorn --workers=1  --worker-class=gthread family_savior.wsgi:application --bind "0.0.0.0:${APP_PORT}"
