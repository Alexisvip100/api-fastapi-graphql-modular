from fastapi import Request
from app.core.database import AsyncSessionLocal

from app.core.redis import redis_client

from app.core.dependencies import get_current_user_graphql

async def get_context(request: Request):
    async with AsyncSessionLocal() as db:
        user = await get_current_user_graphql(request, db)
        yield {
            "db": db,
            "redis": redis_client,
            "request": request,
            "user": user
        }

