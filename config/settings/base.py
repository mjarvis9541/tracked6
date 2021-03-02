import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

with open(BASE_DIR / 'config.json') as f:
    config = json.load(f)

SECRET_KEY = config['SECRET_KEY']

INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    # Project
    'accounts.apps.AccountsConfig',
    'blog.apps.BlogConfig',
    'diaries.apps.DiariesConfig',
    'food.apps.FoodConfig',
    'meals.apps.MealsConfig',
    'profiles.apps.ProfilesConfig',
    'progress.apps.ProgressConfig',
    'utils.apps.UtilsConfig',

    # 3rd-party
    'rest_framework',
]

AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'GMT'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / 'static' # using collectstatic - send static files to
STATICFILES_DIRS = [BASE_DIR / 'static']
# using collectstatic - retreive static files from

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_REDIRECT_URL = 'profiles:profile'
LOGIN_URL = 'accounts:login'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
        # 'rest_framework.permissions.AllowAny', # Set by default
        # 'rest_framework.permissions.IsAuthenticated',
    ],
    # 'DEFAULT_AUTHENTICATION_CLASSES': [
    #     'rest_framework.authentication.SessionAuthentication', # Set by default
    #     'rest_framework.authentication.BasicAuthentication', # Set by default
    #     'rest_framework.authentication.TokenAuthentication',
    # ],
}

