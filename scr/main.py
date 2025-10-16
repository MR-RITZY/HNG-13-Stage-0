from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from httpx import AsyncClient
from datetime import datetime, timezone
from scr.rate_limiter import RateLimiter
from contextlib import asynccontextmanager


from scr.log import error_logger, info_logger
from scr.config import settings
from scr.schema import ResponseReturn
from scr.redis_manager import get_redis

@asynccontextmanager
async def lifespan(app:FastAPI):
    info_logger.info("Setting up Start-ups")
    await get_redis()
    info_logger.info("Start-up Completed Successfully")
    yield
    info_logger.info("Shutting Down: cleaning up resources")
        


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RateLimiter)


@app.get("/me", response_model=ResponseReturn)
async def get_me():
    async with AsyncClient() as client:
        try:
            response = await client.get(settings.CAT_FACT_URL)
            if response.status_code != 200:
                info_logger.info(
                    f"Request Not Successful -- status: {response.status_code}"
                )
            response_json = response.json()
            fact = response_json.get("fact", None)
            if not fact:
                info_logger.info(f"Cat Fact Not Get Returned")
            return {
                "status": "success",
                "user": {
                    "email": settings.EMAIL,
                    "name": settings.NAME,
                    "stack": settings.STACK,
                },
                "timestamp": datetime.now(tz=timezone.utc).isoformat(),
                "fact": fact,
            }
        except Exception as e:
            error_logger.error(f"Unable to fetch cat fact: {e}")
