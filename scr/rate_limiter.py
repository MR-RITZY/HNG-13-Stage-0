from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from limits.aio.storage import RedisStorage
from limits.aio.strategies import SlidingWindowCounterRateLimiter
from limits import RateLimitItemPerMinute


from scr.redis_manager import pool
from scr.config import settings

redis_url = (
    f"redis://{settings.REDIS_USERNAME}:{settings.REDIS_PASSWORD}@"
    f"{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
)

limit_store = RedisStorage(uri=redis_url, connection_pool=pool)
limit_strategy = SlidingWindowCounterRateLimiter(limit_store)
rate_limit_item = RateLimitItemPerMinute(20)


def get_ip(request: Request):
    return request.client.host


class RateLimiter(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        ip = get_ip(request)
        key = f"ratelimit:{ip}"
        allowed = await limit_strategy.hit(rate_limit_item, key)
        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Try again later.",
            )
        return await call_next(request)
