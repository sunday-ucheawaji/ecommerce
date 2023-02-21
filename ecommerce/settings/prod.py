'''Use this for production'''
from .base import *
import dj_database_url


# database
DATABASES = {'default': dj_database_url.config(default=config('DATABASE_URL'))}
ALLOWED_HOSTS += ["*"]
WSGI_APPLICATION = 'ecommerce.wsgi.prod.application'
DEBUG = True


# email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
