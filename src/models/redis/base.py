from contextlib import contextmanager
import aioredis

from src.settings.redis_settings import RedisSettings

redis_db = RedisSettings()


async def get_session():
    host, port, database, password = redis_db.get_params()

    return await aioredis.from_url(f"redis://{host}:{port}/1", password=password)

    #return redis.Redis(host=host, port=port, db=database, password=password)


