#!/bin/bash
APP_PORT=${PORT:-8000}
cd /app/
/opt/venv/bin/gunicorn --workers=3  --worker-class=gthread family_savior.wsgi:application --preload  --bind "0.0.0.0:8000" --timeout 600  