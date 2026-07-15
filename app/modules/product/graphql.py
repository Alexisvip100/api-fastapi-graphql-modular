from uuid import UUID
import strawberry

from app.modules.product.service import ProductService

@strawberry.type
class ProductType:
    id: UUID
    name: str
    description: str
    price: float
    images_products: list[str]

@strawberry.type
class PaginatedProductType:
    total: int
    products: list[ProductType]

@strawberry.type
class ProductQuery:
    @strawberry.field
    async def product(
        self, 
        info: strawberry.Info, 
        search: str | None = None, 
        offset: int = 0, 
        limit: int = 20
    ) -> PaginatedProductType:
        db = info.context["db"]
        redis_client = info.context["redis"]
        res = await ProductService.get_products(redis_client, db, search=search, offset=offset, limit=limit)
        return PaginatedProductType(
            total=res["total"],
            products=[
                ProductType(
                    id=p.id,
                    name=p.name,
                    description=p.description,
                    price=p.price,
                    images_products=p.images_products
                ) for p in res["products"]
            ]
        )

    @strawberry.field
    async def get_product_by_id(self, info: strawberry.Info, id: UUID) -> ProductType | None:
        db = info.context["db"]
        return await ProductService.get_product_by_id(db, id)
