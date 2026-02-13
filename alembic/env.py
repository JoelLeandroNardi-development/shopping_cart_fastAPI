from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from app.core.settings import settings
from app.core.database import Base
from app.catalog.model import CatalogItem
from app.users.model import User
from app.cart.model import Cart, CartItem

config = context.config

fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_online():
    connectable = engine_from_config(
        {
            "sqlalchemy.url": settings.DATABASE_URL
        },
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()