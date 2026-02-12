from fastapi import FastAPI
from app.core.database import Base, engine
from app.middleware import register_middleware

from app.catalog.router import router as catalog_router
from app.users.router import router as users_router
from app.cart.router import router as cart_router

app = FastAPI(title="Shopping Cart API")

Base.metadata.create_all(bind=engine)

register_middleware(app)

app.include_router(catalog_router)
app.include_router(users_router)
app.include_router(cart_router)