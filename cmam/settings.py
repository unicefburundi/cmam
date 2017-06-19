"""
Django settings for cmam project.
Generated by 'django-admin startproject' using Django 1.8.4.
For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.core.urlresolvers import reverse_lazy


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            os.pardir))
PROJECT_ROOT = os.path.abspath(os.path.join(PROJECT_PATH, os.pardir))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'material',
    'material.frontend',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'import_export',
    'rest_framework',
    'django_extensions',
    'django_tables2',
    'drf_multiple_model',
    'django_filters',
    'explorer',
    'djng',
    'bdiadmin',
    'cmam_app',
    'authtools'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'cmam.urls'

SECRET_KEY = 'ch25angeth23i@ssecr1!!$)(etke@%/32y'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
				],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.core.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cmam.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-US'

TIME_ZONE = 'Africa/Bujumbura'

USE_I18N = True

USE_L10N = True

# For translation
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

from django.utils.translation import ugettext_lazy as _

LANGUAGES = (
    ('fr-Fr', _('French')),
    ('en-Us', _('English')),
)

USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(PROJECT_PATH,  'media')

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'staticfiles'),
)


KNOWN_PREFIXES = {
    'REG': 'SELF_REGISTRATION',
    'SRC': 'STOCK_RECU',
    'SSR': 'STOCK_SORTI',
    'RUP': 'RUPTURE',
    'BAL': 'BALANCE',
    'ADM': 'ADMISSION',
    'SRT': 'SORTI',
    'REGM': 'SELF_REGISTRATION_M',
    'SRCM': 'STOCK_RECU_M',
    'SSRM': 'STOCK_SORTI_M',
    'RUPM': 'RUPTURE_M',
    'BALM': 'BALANCE_M',
    'ADMM': 'ADMISSION_M',
    'SRTM': 'SORTI_M',
}

LOGIN_REDIRECT_URL = reverse_lazy("home")

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend', 'rest_framework.filters.SearchFilter',)
}

FAKER_LOCALE = None     # settings.LANGUAGE_CODE is loaded
FAKER_PROVIDERS = None  # faker.DEFAULT_PROVIDERS is loaded (all)


EXPLORER_SCHEMA_EXCLUDE_TABLE_PREFIXES = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'auth.group'
    )

EXPLORER_SCHEMA_INCLUDE_TABLE_PREFIXES = (
    'cmam_ap',
    'bdiadmin')

EXPLORER_PERMISSION_CHANGE = lambda u: u.is_superuser

EXPLORER_DATA_EXPORTERS = [
    ('csv', 'explorer.exporters.CSVExporter'),
    ('excel', 'explorer.exporters.ExcelExporter'),
    ('json', 'explorer.exporters.JSONExporter'),
    ('pdf', 'explorer.exporters.PdfExporter')
    ]

try:
    from localsettings import *
except ImportError:
 pass