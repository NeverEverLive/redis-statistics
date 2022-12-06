from contextlib import contextmanager
import redis

from src.settings.redis_settings import RedisSettings

redis_db = RedisSettings()


def get_session() -> redis.Redis:
    host, port, database, password = redis_db.get_params()

    return redis.Redis(host=host, port=port, db=database, password=password)


