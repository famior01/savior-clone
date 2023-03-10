'''
Basic Celery configuration, including the Celery app instance. This file is
imported by the Celery worker and the Celery beat scheduler. The Celery app 
instance is used to define tasks and schedule periodic tasks.
'''
from __future__ import absolute_import, unicode_literals
import os
from decouple import config
from celery import Celery
from django.conf import settings

production = config('USE_PRODUCTION', cast=bool)
testing = config('TESTING', cast=bool)
if production==True:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'family_savior.settings.production')
elif testing==True:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'family_savior.settings.testing')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'family_savior.settings.local')


app = Celery('family_savior')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# if you want to use local time
# app.conf.enable_utc = False
# app.conf.timezone = settings.TIME_ZONE # 'Asia/karachi'

# beat scheduler
app.conf.beat_schedule = {}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# the debug_task example is a task that dumps its own request information. This is using the new bind=True task option introduced in Celery 3.1 to easily refer to the current task instance.
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')