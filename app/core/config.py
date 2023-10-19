import os

from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """Класс настроек проекта."""

    app_title: str = os.getenv("APP_TITLE", default="QRKot")
    db_url: str = os.getenv("DB_URL", default="sqlite+aiosqlite:///./fastapi.db")
    secret: str = os.getenv("SECRET", default="string")
    admin_email: Optional[EmailStr] = os.getenv(
        "ADMIN_EMAIL", default="admin@example.ru"
    )
    admin_password: Optional[str] = os.getenv("ADMIN_PASSWORD", default="123password")

    class Config:
        env_file = ".env"


settings = Settings()
