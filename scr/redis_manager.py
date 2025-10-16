from coredis import Redis, ConnectionPool
from contextlib import asynccontextmanager

from scr.config import settings
from scr.log import error_logger, info_logger

redis_url = (
    f"redis://{settings.REDIS_USERNAME}:{settings.REDIS_PASSWORD}@"
    f"{settings.REDIS_HOST}:{settings.REDIS_PORT}"
)

pool = ConnectionPool.from_url(
    redis_url,
    max_connections=50,
    idle_check_interval=30,
    decode_responses=True,
    encoding="utf-8",
)

redis_client = Redis(connection_pool=pool)


@asynccontextmanager
async def get_redis():
    try:
        redis_client.ping()
        info_logger.info("Connected to Redis")
        yield redis_client
    except Exception as e:
        error_logger.error("Error Connecting to Redis")
        raise
    finally:
        redis_client.close()
        redis_client.connection_pool.disconnect()
        info_logger("Disconnected from Redis")
