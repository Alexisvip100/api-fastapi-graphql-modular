from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
import json
from redis.asyncio import Redis
from app.modules.favorites.model import FavoriteList
from app.modules.product.model import Product

class FavoriteRepository:
    @staticmethod
    async def _clear_user_favorites_cache(redis_client: Redis, user_id: UUID) -> None:
        try:
            keys = await redis_client.keys(f"favorites_by_user:all:{user_id}:*")
            if keys:
                await redis_client.delete(*keys)
        except Exception as e:
            print(f"Error clearing cache for user {user_id}: {e}")


    @staticmethod
    async def get_favorites_by_user(redis_client: Redis, db: AsyncSession, user_id: UUID, limit: int, offset: int) -> list[FavoriteList]:
        cache_key_favorites = f"favorites_by_user:all:{user_id}:offset:{offset}:limit:{limit}"
        try:
            data_cache = await redis_client.get(cache_key_favorites)
            if data_cache:
                data = json.loads(data_cache)
                favorite_list = []
                for fav in data:
                    products = [
                        Product(
                            id=UUID(p["id"]),
                            name=p["name"],
                            description=p["description"],
                            price=p["price"],
                            images_products=p["images_products"]
                        )
                        for p in fav["products"]
                    ]
                    favorite_list.append(
                        FavoriteList(
                            id=UUID(fav["id"]),
                            name=fav["name"],
                            description=fav["description"],
                            user_id=user_id,
                            products=products
                        )
                    )
                return favorite_list
        except Exception as e:
            print(f"Error getting data from cache: {e}")

        query = select(FavoriteList).where(FavoriteList.user_id == user_id).offset(offset).limit(limit)
        result = await db.execute(query)
        favorites_list = list(result.scalars().all())
        try:
            data_to_cache = [
                {
                    "id": str(fav.id),
                    "name": fav.name,
                    "description": fav.description,
                    "products": [
                        {
                            "id": str(p.id),
                            "name": p.name,
                            "description": p.description,
                            "price": p.price,
                            "images_products": p.images_products
                        }
                        for p in fav.products
                    ]
                }
                for fav in favorites_list
            ]
            await redis_client.setex(cache_key_favorites, 600, json.dumps(data_to_cache))
        except Exception as e:
            print(f"Error setting data in cache: {e}")

        return favorites_list

    @staticmethod
    async def get_by_id(db: AsyncSession, favorite_id: UUID, user_id: UUID) -> FavoriteList | None:
        query = select(FavoriteList).where(
            (FavoriteList.id == favorite_id) & (FavoriteList.user_id == user_id)
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()

  
    @staticmethod
    async def create(redis_client: Redis, db: AsyncSession, favorite_list: FavoriteList) -> FavoriteList:
        await FavoriteRepository._clear_user_favorites_cache(redis_client, favorite_list.user_id)
        db.add(favorite_list)
        await db.commit()
        await db.refresh(favorite_list)
        return favorite_list

    @staticmethod
    async def update(redis_client: Redis, db: AsyncSession, favorite_list: FavoriteList) -> FavoriteList:
        await FavoriteRepository._clear_user_favorites_cache(redis_client, favorite_list.user_id)
        await db.commit()
        await db.refresh(favorite_list)
        return favorite_list

    @staticmethod
    async def delete(redis_client: Redis, db: AsyncSession, favorite_list: FavoriteList) -> None:
        await FavoriteRepository._clear_user_favorites_cache(redis_client, favorite_list.user_id)
        await db.delete(favorite_list)
        await db.commit()
