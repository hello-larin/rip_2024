import redis
from larin_rest import settings

session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)