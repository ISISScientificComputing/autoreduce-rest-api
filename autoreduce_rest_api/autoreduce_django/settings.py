"""
Django settings for autoreduce_django project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
from autoreduce_db.autoreduce_django.settings import DATABASES as autoreduce_db_settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-sm6+=6-6b=r+h4vwi23gs+n(u=o4aji74u^v6$48ed#+$fjn!f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not "AUTOREDUCTION_PRODUCTION" in os.environ
DEBUG_PROPAGATE_EXCEPTIONS = True

DEBUG_HOSTS = "127.0.0.1 localhost reducedev2.isis.cclrc.ac.uk"
PROD_HOSTS = "127.0.0.1 localhost 0.0.0.0 reduce.isis.cclrc.ac.uk"

if DEBUG:
    ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', DEBUG_HOSTS).split()
else:
    ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', PROD_HOSTS).split()

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'autoreduce_db.reduction_viewer',
    'autoreduce_db.instrument',
    'rest_framework',
    'rest_framework.authtoken',
    'autoreduce_rest_api.runs',
    'hurricane',
]

if os.environ.get("TESTING_MYSQL_DB", None) is not None:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            # the default name "test_autoreduce" matches the default database name created
            # by the autoreduce-frontend integration tests. This should not be changed unless
            # pytest's implementation of the naming changes, but if it does, it can be passed through
            # the environment variable as the rest_api is started!
            'NAME': os.environ.get("TESTING_MYSQL_DB_NAME", "test_autoreduce"),
            'USER': "root",
            'PASSWORD': "password",
            'HOST': "127.0.0.1",
            'PORT': "3306",
        }
    }
else:
    DATABASES = autoreduce_db_settings

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'autoreduce_rest_api.autoreduce_django.urls'

WSGI_APPLICATION = 'autoreduce_rest_api.autoreduce_django.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
