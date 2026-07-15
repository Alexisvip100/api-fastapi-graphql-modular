from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.modules.product.model import Product
from app.modules.product.schemas import ProductCreate, ProductUpdate
from app.modules.product.repository import ProductRepository


class ProductService:
    @staticmethod
    async def get_products(redis_client: Redis, db: AsyncSession, search: str | None = None, offset: int = 0, limit: int = 10) -> dict:
        return await ProductRepository.get_all(redis_client, db, search=search, offset=offset, limit=limit)

    @staticmethod
    async def get_product_by_id(db: AsyncSession, product_id: UUID) -> Product | None:
        return await ProductRepository.get_by_id(db, product_id)

    @staticmethod
    async def create_product(db: AsyncSession, product_data: ProductCreate) -> Product:
        new_product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            images_products=product_data.images_products
        )
        return await ProductRepository.create(db, new_product)

    @staticmethod
    async def update_product(db: AsyncSession, product_id: UUID, product_data: ProductUpdate) -> Product | None:
        product = await ProductRepository.get_by_id(db, product_id)
        if not product:
            return None
        
        # Actualiza solo los campos proporcionados
        update_data = product_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(product, key, value)
            
        return await ProductRepository.update(db, product)

    @staticmethod
    async def delete_product(db: AsyncSession, product_id: UUID) -> bool:
        product = await ProductRepository.get_by_id(db, product_id)
        if not product:
            return False
            
        await ProductRepository.delete(db, product)
        return True