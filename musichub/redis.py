import os

from redis import Redis

redis = Redis(host=os.getenv('RD_HOST'),
              port=os.getenv('RD_PORT'))
