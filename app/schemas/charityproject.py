from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CharityProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)


class CharityProjectPatch(CharityProjectCreate):
    pass


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime  # todo исправить поле на created_date
    close_date: Optional[datetime]

    class Config:
        orm_mode = True