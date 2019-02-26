# -*- coding: utf-8 -*-
"""
Production Configurations

- Use djangosecure
- Use Amazon's S3 for storing static files and uploaded media
- Use mailgun to send emails
- Use Redis on Heroku

- Use sentry for error logging


"""
from __future__ import absolute_import, unicode_literals

from boto.s3.connection import OrdinaryCallingFormat
from django.utils import six

import logging


from .common import *  # noqa

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
# SECRET_KEY = env('DJANGO_SECRET_KEY')
SECRET_KEY = 'l^y44io8f!zr^#n(ui099rz+w2(p^ufz3j726-^6)7g2ijcp!k'


# This ensures that Django will be able to detect a secure connection
# properly on Heroku.
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# raven sentry client
# See https://docs.getsentry.com/hosted/clients/python/integrations/django/
INSTALLED_APPS += ['raven.contrib.django.raven_compat', ]

# Use Whitenoise to serve static files
# See: https://whitenoise.readthedocs.io/
WHITENOISE_MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware', ]
MIDDLEWARE = WHITENOISE_MIDDLEWARE + MIDDLEWARE
RAVEN_MIDDLEWARE = ['raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware', ]
MIDDLEWARE = RAVEN_MIDDLEWARE + MIDDLEWARE


# SECURITY CONFIGURATION
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/1.9/ref/middleware/#module-django.middleware.security
# and https://docs.djangoproject.com/ja/1.9/howto/deployment/checklist/#run-manage-py-check-deploy

# set this to 60 seconds and then to 518400 when you can prove it works
SECURE_HSTS_SECONDS = 300
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'SAMEORIGIN'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SECURE_FRAME_DENY = True

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts
# ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['leb-ems.azurewebsites.net', ])
ALLOWED_HOSTS = ['leb-ems.azurewebsites.net', '127.0.0.1', 'ems-new-skin.herokuapp.com']
# END SITE CONFIGURATION

# INSTALLED_APPS += ['gunicorn', ]


# STORAGE CONFIGURATION
# ------------------------------------------------------------------------------
# Uploaded Media Files
# ------------------------
# See: http://django-storages.readthedocs.io/en/latest/index.html
INSTALLED_APPS += ['storages', ]

AZURE_ACCOUNT_NAME = env('AZURE_ACCOUNT_NAME', default='NO_AZURE_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY = env('AZURE_ACCOUNT_KEY', default='NO_AZURE_ACCOUNT_KEY')
AZURE_CONTAINER = env('AZURE_CONTAINER', default='NO_AZURE_CONTAINER')

DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
DEFAULT_FILE_FORMAT = 'xlsx'
DEFAULT_FILE_CONTENT_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
DEFAULT_FILE_CONTENT_LANGUAGE = 'ar'

# Static Assets
# ------------------------
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# COMPRESSOR
# ------------------------------------------------------------------------------
# COMPRESS_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
# COMPRESS_URL = STATIC_URL
# COMPRESS_ENABLED = env.bool('COMPRESS_ENABLED', default=True)
# EMAIL
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL',
                         default='referral_platform <noreply@reffer.uniceflebanon.org>')
EMAIL_SUBJECT_PREFIX = env('DJANGO_EMAIL_SUBJECT_PREFIX', default='[referral_platform] ')
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)

# Anymail with Mailgun
INSTALLED_APPS += ["anymail", ]
ANYMAIL = {
    "MAILGUN_API_KEY": env('DJANGO_MAILGUN_API_KEY', default='NO_MAILGUN_API_KEY'),
}
EMAIL_BACKEND = "anymail.backends.mailgun.MailgunBackend"

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See:
# https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.cached.Loader
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader', ]),
]

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
DATABASES['default'] = env.db('DATABASE_URL')
# DATABASES['default'] = 'postgres://dbbsanytmxkyzd:b10e9d200d7acb25a26ff7d84d0aa338944cd47e0503a29ad9e63c0e1eab8df5@ec2-50-16-196-238.compute-1.amazonaws.com:5432/d3pr7hqep9t1bk',

# if env.bool('DATABASE_SSL_ENABLED', default=False):
    # DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}
    # DATABASES['default']['OPTIONS']['sslmode'] = 'require'

# CACHING
# ------------------------------------------------------------------------------
# Heroku URL does not pass the DB number, so we parse it in
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': '{0}/{1}'.format(env('REDIS_URL', default='redis://127.0.0.1:6379'), 0),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'IGNORE_EXCEPTIONS': True,  # mimics memcache behavior.
                                        # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
        }
    }
}


# Sentry Configuration
# SENTRY_DSN = env('DJANGO_SENTRY_DSN')
SENTRY_DSN = 'https://8de7f8a6d22e45989f48d078de430dff:65abf371e2614f65b72d3f154cf5a071@sentry.io/1201926'
SENTRY_CLIENT = env('DJANGO_SENTRY_CLIENT', default='raven.contrib.django.raven_compat.DjangoClient')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
    },
}
SENTRY_CELERY_LOGLEVEL = env.int('DJANGO_SENTRY_LOG_LEVEL', logging.INFO)
RAVEN_CONFIG = {
    'CELERY_LOGLEVEL': env.int('DJANGO_SENTRY_LOG_LEVEL', logging.INFO),
    'DSN': SENTRY_DSN
}

# Custom Admin URL, use {% url 'admin:index' %}
# ADMIN_URL = env('DJANGO_ADMIN_URL')


# WEBPACK
# ------------------------------------------------------------------------------
# Webpack Production Stats file
# STATS_FILE = ROOT_DIR('webpack-stats-production.json')
# Webpack config
# WEBPACK_LOADER = {
#     'DEFAULT': {
#         'BUNDLE_DIR_NAME': 'referral_platform/static/referral_platform/dist/',
#         'STATS_FILE': STATS_FILE
#     }
# }

# DEBUG_MODE:
DEBUG = env.bool('DJANGO_DEBUG', False)


# Your production stuff: Below this line define 3rd party library settings
