'''Use this for development'''

from .base import *

DEBUG = config('DEBUG', cast=bool)
WSGI_APPLICATION = 'ecommerce.wsgi.dev.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

ALLOWED_HOSTS += ["*"]