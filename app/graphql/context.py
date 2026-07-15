from fastapi import Request
from app.core.database import AsyncSessionLocal

from app.core.redis import redis_client

async def get_context(request: Request):
    async with AsyncSessionLocal() as db:
        yield {"db": db, "redis": redis_client, "request": request}

