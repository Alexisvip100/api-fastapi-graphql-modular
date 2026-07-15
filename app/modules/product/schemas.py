from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    images_products: list[str] = []
    model_config = ConfigDict(from_attributes=True)


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    images_products: list[str] | None = None
    model_config = ConfigDict(from_attributes=True)



class ProductResponse(BaseModel):
    id: UUID
    name: str
    description: str
    price: float
    images_products: list[str]
    model_config = ConfigDict(from_attributes=True)


class PaginatedProductResponse(BaseModel):
    total: int
    products: list[ProductResponse]