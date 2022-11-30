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

# email

EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_HOST_USER = '80f3c9b6c66f00'
EMAIL_HOST_PASSWORD = 'c372c0823a508d'
EMAIL_PORT = '2525'
