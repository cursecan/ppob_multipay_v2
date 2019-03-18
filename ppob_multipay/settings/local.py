import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'no-reply@warungid.com'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# JWT Django
# https://getblimp.github.io/django-rest-framework-jwt/#additional-settings

JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(minutes=5),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(hours=1),
}