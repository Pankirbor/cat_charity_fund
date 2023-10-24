from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field

from app.constants import GREATER_THAN


class DonationCreate(BaseModel):
    """Класс схемы для создания пожертвования."""

    full_amount: int = Field(gt=GREATER_THAN)
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationDBForUser(DonationCreate):
    """Класс схемы для представления пожертвования
    в ответе на запрос получения всех объектов для пользователя."""

    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDBAll(DonationDBForUser):
    """Класс схемы для представления пожертвования
    в ответе на запрос получения всех объектов для суперюзера."""

    user_id: Optional[int]
    comment: Optional[str]
    invested_amount: int
    fully_invested: bool = Field(False)
