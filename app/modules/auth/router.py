from app.modules.auth.service import AuthService
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.auth.schemas import LoginRequest, Token
from app.modules.user.schemas import (
    UserCreate,
    UserResponse,
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@router.post(
    "/register",
    response_model=UserResponse,
)
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await AuthService.register(
            db,
            user,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

@router.post(
    "/login",
    response_model=Token,
)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await AuthService.login(
            db,
            data.email,
            data.password,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )