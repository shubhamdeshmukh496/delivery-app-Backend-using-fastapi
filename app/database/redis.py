from redis.asyncio import Redis
from app.config import db_settings
# Create Redis connection (we can make this a singleton-like object)
redis_client = Redis(
    host=db_settings.REDIS_HOST,
    port=db_settings.REDIS_PORT,
    decode_responses=True
)

async def add_jti_to_blacklist(jti: str):
    await redis_client.set(jti, "blacklisted")

async def is_jti_blacklisted(jti: str) -> bool:
    return await redis_client.exists(jti) > 0
