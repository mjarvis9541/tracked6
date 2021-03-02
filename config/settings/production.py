from .base import *

DEBUG = False

ALLOWED_HOSTS = ['']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config['PRODUCTION_DB_NAME'],
        'USER': config['PRODUCTION_DB_USER'],
        'PASSWORD': config['PRODUCTION_DB_PASS'],
        'HOST': config['PRODUCTION_DB_HOST'],
        'PORT': config['PRODUCTION_DB_PORT'],
    }
}

EMAIL_BACKEND = ''