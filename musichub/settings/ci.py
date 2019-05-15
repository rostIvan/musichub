import os

from musichub.settings import BASE_DIR

SECRET_KEY = '(!w!77_&@puvmxhz*b16xtfiuyjh9o8zfv2%i!v5$mu8$z2x*h'
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
