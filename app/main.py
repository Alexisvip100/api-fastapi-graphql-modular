from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from app.graphql.schema import schema
from app.graphql.context import get_context
from app.modules.product.router import router_product
from app.modules.auth.router import router as auth_router
from app.modules.favorites.router import router as favorites_router
from app.core.database import engine, Base
from app.modules.product.model import Product
from app.modules.user.model import User
from app.modules.favorites.model import FavoriteList


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crea las tablas en la base de datos si no existen
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="User store", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graphql_app = GraphQLRouter(schema, context_getter=get_context)

app.include_router(
    graphql_app,
    prefix="/graphql"
)
app.include_router(router_product)
app.include_router(auth_router)
app.include_router(favorites_router)