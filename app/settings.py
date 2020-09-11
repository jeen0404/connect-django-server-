"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ma_&u12oq%gy8zqd4&b8yjb3x1!$fyhmopbkz&pwquq@5oim*6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

INTERNAL_IPS = [
    '127.0.0.1',
]
# Application definition

INSTALLED_APPS = [
    'channels',
    'chat',
    'post',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'rest_framework',
    'rest_framework.authtoken',
    'connections',
    "fcm_django",
    "notification",
    'django_cassandra_engine',
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

# Channels
ASGI_APPLICATION = 'app.routing.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
            'capacity': 15000,
            'expiry': 1,
        },
    },
}

# accounts
AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = [
    'accounts.backend.PhoneBackend',
    'django.contrib.auth.backends.ModelBackend'
]

# rest framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'PAGINATE_BY': 10
}
# otp config
PHONE_LOGIN_ATTEMPTS = 50
PHONE_LOGIN_OTP_LENGTH = 4
PHONE_LOGIN_OTP_HASH_ALGORITHM = 'sha256'
PHONE_LOGIN_DEBUG = True

# fcm
FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY": "AAAA0dYJtt0:APA91bFyFhvkB7j-SbZVS6h5CYsPK2JMrdDqijKe8_IoR1PVfgzFV6NscaxOVtqVV8OJf3WvxHQB1UCQSaRlqtX3SqBi7gR6J8x_g-qAcRp2DJZ3DVE_6PS85lPQQAPNA4n-Y4IKtrWD"
}

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'connect',
        'USER': 'connect',
        'PASSWORD': 'jivan0404',
        'HOST': '127.0.0.1',
        "PORT": "5432"
    },
    'cassandra': {
        'ENGINE': 'django_cassandra_engine',
        'NAME': 'connect',
        'TEST_NAME': 'connect',
        'HOST': '127.0.0.1',
        "PORT": '9042',
        'OPTIONS': {
            'replication': {
                'strategy_class': 'SimpleStrategy',
                'replication_factor': 3
            }
        }
    }
}
CASSANDRA_FALLBACK_ORDER_BY_PYTHON = True

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "example"
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'



