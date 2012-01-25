import os
cwd = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

CACHE_TIMEOUT = 15
CACHE_PREFIX = str('fecto-prod')
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '127.0.0.1:6379',
        'OPTIONS': {
            'DB': 1,
            #'PASSWORD': 'yadayada',
        },
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fecto-prod',
        'USER': 'fecto-prod',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

COMPRESS = True

INSTALLED_APPS = (
)