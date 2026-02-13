from fastapi import FastAPI
from app.core.database import Base, engine

from app.users.router import router as users_router
from app.catalog.router import router as catalog_router
from app.cart.router import router as cart_router

app = FastAPI()

app.include_router(users_router)
app.include_router(catalog_router)
app.include_router(cart_router)