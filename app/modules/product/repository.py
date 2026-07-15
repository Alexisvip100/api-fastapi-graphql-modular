from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from redis.asyncio import Redis
from app.modules.product.model import Product
import json


class ProductRepository:
    @staticmethod
    async def get_all(redis_client: Redis, db: AsyncSession, search: str | None = None, offset: int = 0, limit: int = 20) -> dict:
        cache_key = f"products:all:search:{search or ''}:offset:{offset}:limit:{limit}"
        try:
            cached_data = await redis_client.get(cache_key)
            if cached_data:
                data = json.loads(cached_data)
                cached_products = [
                    Product(
                        id=UUID(product['id']),
                        name=product['name'],
                        description=product['description'],
                        price=product['price'],
                        images_products=product['images_products']
                    ) for product in data['products']
                ]
                return {
                    "total": data['total'],
                    "products": cached_products,
                }
        except Exception as e:
            print(f"Error getting data from cache: {e}")

        # Base query for products
        query = select(Product)
        # Base query for count
        count_query = select(func.count(Product.id))

        if search:
            filter_cond = (
                Product.name.ilike(f"%{search}%") | 
                Product.description.ilike(f"%{search}%")
            )
            query = query.where(filter_cond)
            count_query = count_query.where(filter_cond)

        # Get total count
        total_products = await db.scalar(count_query)

        # Get paginated products
        query = query.offset(offset).limit(limit)
        result = await db.execute(query)
        products_list = list(result.scalars().all())

        # Save to Redis
        try:
            data_to_cache = {
                "total": total_products or 0,
                "products": [
                    {
                        "id": str(p.id),
                        "name": p.name,
                        "description": p.description,
                        "price": p.price,
                        "images_products": p.images_products
                    }
                    for p in products_list
                ]
            }
            await redis_client.setex(cache_key, 600, json.dumps(data_to_cache))
        except Exception as e:
            print(f"Error setting data in cache: {e}")

        return {
            "total": total_products or 0,
            "products": products_list
        }

    @staticmethod
    async def get_by_id(db: AsyncSession, product_id: UUID) -> Product | None:
        query = select(Product).where(Product.id == product_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, product: Product) -> Product:
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product

    @staticmethod
    async def update(db: AsyncSession, product: Product) -> Product:
        await db.commit()
        await db.refresh(product)
        return product

    @staticmethod
    async def delete(db: AsyncSession, product: Product) -> None:
        await db.delete(product)
        await db.commit()
