#!/bin/bash
cd /app/
/opt/venv/bin/celery -A family_savior worker -l INFO 
