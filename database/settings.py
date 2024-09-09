import os
from pathlib import Path

LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"
USE_TZ = True

INSTALLED_APPS = [
    'database.apps.DatabaseConfig',
]

ALLOWED_HOSTS = ['*']
DEBUG = True

DJANGO_SETTINGS_MODULE = 'database.settings'

BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
