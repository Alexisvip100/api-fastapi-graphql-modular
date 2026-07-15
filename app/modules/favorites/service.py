from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.favorites.model import FavoriteList
from app.modules.product.model import Product
from app.modules.favorites.repository import FavoriteRepository
from app.modules.product.repository import ProductRepository
from app.modules.favorites.schemas import FavoritesCreate, FavoriteUpdate
from redis.asyncio import Redis

class FavoriteService:
    @staticmethod
    async def get_favorites_by_user(redis_client: Redis, db: AsyncSession, user_id: UUID, limit: int = 20, offset: int = 0) -> list[FavoriteList]:
        return await FavoriteRepository.get_favorites_by_user(redis_client, db, user_id, limit, offset)

    @staticmethod
    async def get_favorite_list_by_id(db: AsyncSession, favorite_id: UUID, user_id: UUID) -> FavoriteList | None:
        return await FavoriteRepository.get_by_id(db, favorite_id, user_id)

    @staticmethod
    async def create_favorite_list(db: AsyncSession, user_id: UUID, favorite_data: FavoritesCreate, product_list: list[Product] | None = None) -> FavoriteList:
        new_list = FavoriteList(
            user_id=user_id,
            name=favorite_data.name,
            description=favorite_data.description,
            products=product_list or []
        )
        return await FavoriteRepository.create(db, new_list)

    @staticmethod
    async def update_favorite_list(
        db: AsyncSession, favorite_id: UUID, user_id: UUID, favorite_data: FavoriteUpdate
    ) -> FavoriteList | None:
        favorite_list = await FavoriteRepository.get_by_id(db, favorite_id, user_id)
        if not favorite_list:
            return None

        update_data = favorite_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(favorite_list, key, value)

        return await FavoriteRepository.update(db, favorite_list)

    @staticmethod
    async def delete_favorite_list(db: AsyncSession, favorite_id: UUID, user_id: UUID) -> bool:
        favorite_list = await FavoriteRepository.get_by_id(db, favorite_id, user_id)
        if not favorite_list:
            return False

        await FavoriteRepository.delete(db, favorite_list)
        return True

    @staticmethod
    async def add_product_to_favorites(
        db: AsyncSession, favorite_id: UUID, user_id: UUID, product_id: UUID
    ) -> FavoriteList | None:
        # Fetch the favorite list and ensure it belongs to the user
        favorite_list = await FavoriteRepository.get_by_id(db, favorite_id, user_id)
        if not favorite_list:
            return None

        # Fetch the product to check if it exists
        product = await ProductRepository.get_by_id(db, product_id)
        if not product:
            raise ValueError("Product not found")

        # Check if product is already in favorites list to avoid duplicates
        if product not in favorite_list.products:
            favorite_list.products.append(product)
            await FavoriteRepository.update(db, favorite_list)

        return favorite_list

    @staticmethod
    async def remove_product_from_favorites(
        db: AsyncSession, favorite_id: UUID, user_id: UUID, product_id: UUID
    ) -> FavoriteList | None:
        favorite_list = await FavoriteRepository.get_by_id(db, favorite_id, user_id)
        if not favorite_list:
            return None

        product = await ProductRepository.get_by_id(db, product_id)
        if not product:
            raise ValueError("Product not found")

        if product in favorite_list.products:
            favorite_list.products.remove(product)
            await FavoriteRepository.update(db, favorite_list)

        return favorite_list