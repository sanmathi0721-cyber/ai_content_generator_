INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'generator',
]

import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'replace-this-with-your-secret-key'
DEBUG = True
ALLOWED_HOSTS = ['*']

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
