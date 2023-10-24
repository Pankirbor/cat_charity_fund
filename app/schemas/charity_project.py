from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field

from app.constants import (
    GREATER_THAN,
    MAX_LENGTH,
    MIN_LENGTH,
)


class CharityProjectCreate(BaseModel):
    """Класс схемы для создания фонда."""

    name: str = Field(
        min_length=MIN_LENGTH,
        max_length=MAX_LENGTH,
    )
    description: str = Field(min_length=MIN_LENGTH)
    full_amount: int = Field(gt=GREATER_THAN)

    class Config:
        extra = Extra.forbid


class CharityProjectPatch(CharityProjectCreate):
    """Класс схемы для обновления данных фонда."""

    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[int]


class CharityProjectDB(CharityProjectCreate):
    """Класс схемы для представления фонда
    в ответе на запрос получения всех объектов."""

    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime

    class Config:
        orm_mode = True


class CharityProjectDBPatchDelete(CharityProjectDB):
    """Класс схемы для представления фонда
    в ответе на запрос обновления или удаления."""

    close_date: Optional[datetime]
