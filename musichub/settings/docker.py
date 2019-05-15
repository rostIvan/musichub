import os

from musichub.settings import BASE_DIR

ALLOWED_HOSTS = ['*']
DEBUG = False

STATIC_ROOT = "/opt/services/musichub/static/"
MEDIA_ROOT = "/opt/services/musichub/media/"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('PG_DB'),
        'USER': os.getenv('PG_USER'),
        'PASSWORD': os.getenv('PG_PASSWORD'),
        'HOST': os.getenv('PG_HOST'),
        'PORT': os.getenv('PG_PORT_IN')
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': f'{BASE_DIR}/../logs/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'propagate': True,
        },
    },
}
