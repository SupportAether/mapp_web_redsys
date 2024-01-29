"""
Django settings for mapp_web_redsys project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&c#@g^b3c(3as09d@^!_*h*r0h+s*ng3t@+jn*!3n2zh06*hqh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS += ('sermepa', 'sermepa_test')

# PAYMENT_VARIANTS = {
#     'redsys': ('payments_redsys.RedsysProvider', {
#         'merchant_code': '014407381',
#         'terminal': '2',
#         'shared_secret': 'sq7HjrUOBfKmC576ILgskD5srU870gJ7',
#     })
# }

# CHECKOUT_PAYMENT_CHOICES = [('redsys', 'Redsys')]

# if any('redsys' in provider for provider in CHECKOUT_PAYMENT_CHOICES):
#     INSTALLED_APPS.append('payments_redsys')

SERMEPA_URL_PRO = 'https://sis.redsys.es/sis/realizarPago'
SERMEPA_URL_TEST = 'https://sis-t.redsys.es:25443/sis/realizarPago'
SERMEPA_MERCHANT_CODE = '999008881' #comercio de test
SERMEPA_TERMINAL = '001'
SERMEPA_SECRET_KEY = 'sq7HjrUOBfKmC576ILgskD5srU870gJ7'
SERMEPA_BUTTON_IMG = '/site_media/_img/targets.jpg'
SERMEPA_CURRENCY = '978' #Euros
SERMEPA_SITE_DOMAIN = "https://prueba.com"
SERMEPA_SIGNATURE_VERSION = 'HMAC_SHA256_V1'
DEBUG = True
SERMEPA_BUTTON_TEXT = 'Pay now'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mapp_web_redsys.urls'

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

WSGI_APPLICATION = 'mapp_web_redsys.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'