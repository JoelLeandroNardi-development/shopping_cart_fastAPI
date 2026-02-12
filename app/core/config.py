from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./shopping_cart.db"

    class Config:
        env_file = ".env"

settings = Settings()