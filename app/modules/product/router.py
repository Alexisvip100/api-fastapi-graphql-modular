from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.modules.product.schemas import ProductCreate, ProductUpdate, ProductResponse, PaginatedProductResponse
from app.modules.product.service import ProductService
from app.core.redis import get_redis
from redis.asyncio import Redis

router_product = APIRouter()


@router_product.get("/api/v1/products", response_model=PaginatedProductResponse)
async def get_products(
    search: str | None = None,
    offset: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    redis_client: Redis = Depends(get_redis),
    current_user = Depends(get_current_user)
):
    try:
        results = await ProductService.get_products(redis_client, db, search=search, offset=offset, limit=limit)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo productos: {str(e)}"
        )


@router_product.get("/api/v1/products/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    product = await ProductService.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    return product


@router_product.post("/api/v1/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    redis_client: Redis = Depends(get_redis),
    current_user = Depends(get_current_user)
):
    try:
        new_product = await ProductService.create_product(redis_client, db, product_data)
        return new_product
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear el producto: {str(e)}"
        )


@router_product.put("/api/v1/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: UUID,
    product_data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    redis_client: Redis = Depends(get_redis),
    current_user = Depends(get_current_user)
):
    updated_product = await ProductService.update_product(redis_client, db, product_id, product_data)
    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado o no se pudo actualizar"
        )
    return updated_product


@router_product.delete("/api/v1/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
    redis_client: Redis = Depends(get_redis),
    current_user = Depends(get_current_user)
):
    success = await ProductService.delete_product(redis_client, db, product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado o no se pudo eliminar"
        )
    return None
