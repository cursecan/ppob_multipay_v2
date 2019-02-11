from .base import *
from decouple import config
import datetime

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWD'),
        'HOST': config('DB_HOST'),
        'PORT': '',
    }
}

# JWT Django
# https://getblimp.github.io/django-rest-framework-jwt/#additional-settings

JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(minutes=5),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(hours=1),
}