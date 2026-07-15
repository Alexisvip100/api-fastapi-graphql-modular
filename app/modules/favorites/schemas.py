from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.modules.product.schemas import ProductResponse

class FavoritesCreate(BaseModel):
    name: str
    description: str | None = None

class FavoritesResponse(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    description: str | None = None
    created_at: datetime
    products: list[ProductResponse] = []

    model_config = ConfigDict(from_attributes=True)

class PaginationFavorites(BaseModel):
    total: int
    favorites: list[FavoritesResponse]

class FavoriteUpdate(BaseModel):
    name: str | None = None
    description: str | None = None