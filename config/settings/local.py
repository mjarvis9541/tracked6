from .base import *

DEBUG = True

ALLOWED_HOSTS = []

INTERNAL_IPS = ['127.0.0.1']

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config['LOCAL_DB_NAME'],
        'USER': config['LOCAL_DB_USER'],
        'PASSWORD': config['LOCAL_DB_PASS'],
        'HOST': config['LOCAL_DB_HOST'],
        'PORT': config['LOCAL_DB_PORT'],
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'