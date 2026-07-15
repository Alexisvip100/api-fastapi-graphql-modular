from uuid import UUID
import strawberry
from app.modules.product.graphql import ProductType
from app.modules.favorites.service import FavoriteService
from app.modules.favorites.schemas import FavoritesCreate

@strawberry.type
class FavoriteType:
    id: UUID
    name: str
    description: str | None
    created_at: str
    products: list[ProductType]

@strawberry.type
class FavoritesQuery:
    @strawberry.field
    async def favorites(self, info: strawberry.Info, limit: int = 20, offset: int = 0) -> list[FavoriteType]:
        db = info.context["db"]
        current_user = info.context["user"]
        if not current_user:
            raise ValueError("401: Could not validate credentials")
            
        redis_client = info.context["redis"]
        fav_lists = await FavoriteService.get_favorites_by_user(redis_client, db, current_user.id, limit, offset)
        return [
            FavoriteType(
                id=f.id,
                name=f.name,
                description=f.description,
                created_at=f.created_at.isoformat() if f.created_at else "",
                products=[
                    ProductType(
                        id=p.id,
                        name=p.name,
                        description=p.description,
                        price=p.price,
                        images_products=p.images_products
                    ) for p in f.products
                ]
            ) for f in fav_lists
        ]

    @strawberry.field
    async def get_favorite_list_by_id(self, info: strawberry.Info, id: UUID) -> FavoriteType | None:
        db = info.context["db"]
        current_user = info.context["user"]
        if not current_user:
            raise ValueError("401: Could not validate credentials")
            
        fav_list = await FavoriteService.get_favorite_list_by_id(db, id, current_user.id)
        if not fav_list:
            return None
        return FavoriteType(
            id=fav_list.id,
            name=fav_list.name,
            description=fav_list.description,
            created_at=fav_list.created_at.isoformat() if fav_list.created_at else "",
            products=[
                ProductType(
                    id=p.id,
                    name=p.name,
                    description=p.description,
                    price=p.price,
                    images_products=p.images_products
                ) for p in fav_list.products
            ]
        )

@strawberry.type
class FavoritesMutation:
    @strawberry.mutation
    async def create_favorite_list(
        self, 
        info: strawberry.Info, 
        name: str, 
        description: str | None = None
    ) -> FavoriteType:
        db = info.context["db"]
        current_user = info.context["user"]
        redis_client = info.context["redis"]
        if not current_user:
            raise ValueError("401: Could not validate credentials")
            
        fav_data = FavoritesCreate(name=name, description=description)
        new_list = await FavoriteService.create_favorite_list(db, redis_client, current_user.id, fav_data)
        
        return FavoriteType(
            id=new_list.id,
            name=new_list.name,
            description=new_list.description,
            created_at=new_list.created_at.isoformat() if new_list.created_at else "",
            products=[]
        )

    @strawberry.mutation
    async def delete_favorite_list(self, info: strawberry.Info, id: UUID) -> bool:
        db = info.context["db"]
        current_user = info.context["user"]
        if not current_user:
            raise ValueError("401: Could not validate credentials")
            
        return await FavoriteService.delete_favorite_list(db, id, current_user.id)

    @strawberry.mutation
    async def add_product_to_favorites(
        self, 
        info: strawberry.Info, 
        favorite_id: UUID, 
        product_id: UUID
    ) -> FavoriteType:
        db = info.context["db"]
        current_user = info.context["user"]
        if not current_user:
            raise ValueError("401: Could not validate credentials")
            
        updated_list = await FavoriteService.add_product_to_favorites(
            db, favorite_id, current_user.id, product_id
        )
        if not updated_list:
            raise ValueError("Favorite list not found or unauthorized")
            
        return FavoriteType(
            id=updated_list.id,
            name=updated_list.name,
            description=updated_list.description,
            created_at=updated_list.created_at.isoformat() if updated_list.created_at else "",
            products=[
                ProductType(
                    id=p.id,
                    name=p.name,
                    description=p.description,
                    price=p.price,
                    images_products=p.images_products
                ) for p in updated_list.products
            ]
        )

    @strawberry.mutation
    async def remove_product_from_favorites(
        self, 
        info: strawberry.Info, 
        favorite_id: UUID, 
        product_id: UUID
    ) -> FavoriteType:
        db = info.context["db"]
        current_user = info.context["user"]
        if not current_user:
            raise ValueError("401: Could not validate credentials")
            
        updated_list = await FavoriteService.remove_product_from_favorites(
            db, favorite_id, current_user.id, product_id
        )
        if not updated_list:
            raise ValueError("Favorite list not found or unauthorized")
            
        return FavoriteType(
            id=updated_list.id,
            name=updated_list.name,
            description=updated_list.description,
            created_at=updated_list.created_at.isoformat() if updated_list.created_at else "",
            products=[
                ProductType(
                    id=p.id,
                    name=p.name,
                    description=p.description,
                    price=p.price,
                    images_products=p.images_products
                ) for p in updated_list.products
            ]
        )
