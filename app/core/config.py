from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = "QRKot"
    db_url: str = "sqlite+aiosqlite:///./fastapi.db"
    secret: str = "SECRET"
    admin_email: Optional[EmailStr] = "ADMIN_EMAIL"
    admin_password: Optional[str] = "ADMIN_PASSWORD"

    class Config:
        env_file = ".env"


settings = Settings()
