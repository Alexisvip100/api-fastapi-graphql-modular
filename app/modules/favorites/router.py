from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.redis import get_redis
from redis.asyncio import Redis
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.modules.user.model import User
from app.modules.favorites.schemas import (
    FavoritesCreate,
    FavoritesResponse,
    FavoriteUpdate,
)
from app.modules.favorites.service import FavoriteService

router = APIRouter(
    prefix="/api/v1/favorites",
    tags=["Favorites"],
)

@router.post(
    "",
    response_model=FavoritesResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_favorite_list(
    favorite_data: FavoritesCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    redis_client: Redis = Depends(get_redis),
):
    try:
        return await FavoriteService.create_favorite_list(
            redis_client=redis_client,
            db=db,
            user_id=current_user.id,
            favorite_data=favorite_data
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear la lista de favoritos: {str(e)}"
        )

@router.get(
    "",
    response_model=list[FavoritesResponse],
)
async def get_favorites(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    redis_client: Redis = Depends(get_redis),
    limit: int | None = 20,
    offset: int | None = 0
):
    try:
        return await FavoriteService.get_favorites_by_user(redis_client, db, current_user.id, limit, offset)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las listas de favoritos: {str(e)}"
        )

@router.get(
    "/{favorite_id}",
    response_model=FavoritesResponse,
)
async def get_favorite_list_by_id(
    favorite_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    favorite_list = await FavoriteService.get_favorite_list_by_id(
        db=db,
        favorite_id=favorite_id,
        user_id=current_user.id
    )
    if not favorite_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lista de favoritos no encontrada"
        )
    return favorite_list

@router.put(
    "/{favorite_id}",
    response_model=FavoritesResponse,
)
async def update_favorite_list(
    favorite_id: UUID,
    favorite_data: FavoriteUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    redis_client: Redis = Depends(get_redis),
):
    updated_list = await FavoriteService.update_favorite_list(
        redis_client=redis_client,
        db=db,
        favorite_id=favorite_id,
        user_id=current_user.id,
        favorite_data=favorite_data
    )
    if not updated_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lista de favoritos no encontrada o no se pudo actualizar"
        )
    return updated_list

@router.delete(
    "/{favorite_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_favorite_list(
    favorite_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    redis_client: Redis = Depends(get_redis),
):
    success = await FavoriteService.delete_favorite_list(
        redis_client=redis_client,
        db=db,
        favorite_id=favorite_id,
        user_id=current_user.id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lista de favoritos no encontrada o no se pudo eliminar"
        )
    return None

@router.post(
    "/{favorite_id}/products/{product_id}",
    response_model=FavoritesResponse,
)
async def add_product_to_favorites(
    favorite_id: UUID,
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    redis_client: Redis = Depends(get_redis),
):
    try:
        favorite_list = await FavoriteService.add_product_to_favorites(
            redis_client=redis_client,
            db=db,
            favorite_id=favorite_id,
            user_id=current_user.id,
            product_id=product_id
        )
        if not favorite_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lista de favoritos no encontrada"
            )
        return favorite_list
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al agregar producto a favoritos: {str(e)}"
        )

@router.delete(
    "/{favorite_id}/products/{product_id}",
    response_model=FavoritesResponse,
)
async def remove_product_from_favorites(
    favorite_id: UUID,
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    redis_client: Redis = Depends(get_redis),
):
    try:
        favorite_list = await FavoriteService.remove_product_from_favorites(
            redis_client=redis_client,
            db=db,
            favorite_id=favorite_id,
            user_id=current_user.id,
            product_id=product_id
        )
        if not favorite_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lista de favoritos no encontrada"
            )
        return favorite_list
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al remover producto de favoritos: {str(e)}"
        )