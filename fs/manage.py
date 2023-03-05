#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from decouple import config

def main():
    """Run administrative tasks."""
    production = config('USE_PRODUCTION', cast=bool)
    testing = config('TESTING', cast=bool)
    if production==True:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'family_savior.settings.production')
    elif testing==True:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'family_savior.settings.testing')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'family_savior.settings.local')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
