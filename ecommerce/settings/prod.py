'''Use this for production'''
from .base import *
import dj_database_url


# database
DATABASES =  { 'default': dj_database_url.config(default=config('DATABASE_URL'))}
ALLOWED_HOSTS += ["*"]
WSGI_APPLICATION = 'ecommerce.wsgi.prod.application'
DEBUG = True