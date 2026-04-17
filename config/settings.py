import os
from pathlib import Path

import environ
import certifi

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
                  DEBUG=(bool, False),
                  DEBUG_TOOLBAR=(bool, False),
)

environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')
DEBUG_TOOLBAR = env('DEBUG_TOOLBAR')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'pages:home'
LOGOUT_REDIRECT_URL = 'users:login'

ADMIN_URL = os.getenv('ADMIN_URL', 'admin/')

INTERNAL_IPS = env('INTERNAL_IPS').split(',')

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")

AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'all'
AWS_QUERYSTRING_AUTH = True

AWS_S3_ADDRESSING_STYLE = "virtual"
AWS_S3_SIGNATURE_VERSION = "s3v4"

AWS_S3_VERIFY = certifi.where()

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'core.apps.tests.apps.TestsConfig',
    'core.apps.users.apps.UsersConfig',
    'core.services',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'core.project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.services.context_processors.common_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.project.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('POSTGRES_NAME'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
    }
}


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


LANGUAGE_CODE = env('LANGUAGE_CODE')

TIME_ZONE = env('TIME_ZONE')

USE_I18N = True

USE_TZ = True

STATIC_URL = env('STATIC_URL')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'
