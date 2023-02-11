#!/bin/bash
cd /app/
/opt/venv/bin/celery -A family_savior worker --without-heartbeat --without-gossip --without-mingle -l INFO  -P eventlet -c 1000
