"""
Django common settings for all environments in Fecto
For comments and help, check out the upstream.py settings file.
"""

import os
cwd = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

TIME_ZONE = 'Europe/Oslo'

STATIC_ROOT = cwd + '/static'

STATICFILES_DIRS = (
    cwd + '/static_src',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# FIXME, import this from somewhere..
SECRET_KEY = 's_^%8=qs+q@ae@y@g-6--+0z2gk9tl_vg_+*p1bxmy2=g8)x3='

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_hosts.middleware.HostsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'reversion.middleware.RevisionMiddleware', # After TransactionMiddleware
)

ROOT_URLCONF = 'fecto.urls'
ROOT_HOSTCONF = 'hosts'
DEFAULT_HOST = 'fecto'


TEMPLATE_DIRS = (
    cwd + '/templates',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.static',
    'django.core.context_processors.debug',
    'django.contrib.messages.context_processors.messages',
)

SOUTH_AUTO_FREEZE_APP = True

INSTALLED_APPS = (
    # Admin specific stuff
    'django.contrib.admin',

    # Documentation
    'django.contrib.admindocs',

    # Static configuration
    'apps.siteconfig',

    # Misc
    'django_hosts',
    'south',
    'reversion',
    #'treemenus',
    'django_extensions',
    'djangorestframework',
    #'navigen', # Not yet ready, but might use it later
    'compressor',


    # FIXME, autoimport apps with own config
    'apps.contact',
    'apps.serverinfo',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },

        # Used by django-extension and runserver_plus
        'werkzeug': {
            'handlers': ['console'],
        },
    }
}

