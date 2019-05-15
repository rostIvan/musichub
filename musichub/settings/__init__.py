from .default import *

environment = os.getenv('APP_ENVIRONMENT', 'LOCAL').upper()

if environment == 'LOCAL':
    from .local import *
elif environment == 'PRODUCTION':
    from .production import *
elif environment == 'CI':
    from .ci import *
elif environment == 'DOCKER':
    from .docker import *
