from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "api-bot-austin"
    version: str = "0.1.0"
    database_url: str = "sqlite:///./ndpd_dev.db"
    telegram_bot_token: str | None = None
    environment: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
