import redis.asyncio as redis
from app.core.config import settings

# Crea el cliente asíncrono de Redis con decode_responses=True para retornar strings en lugar de bytes
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

async def get_redis():
    yield redis_client
