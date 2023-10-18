from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field


class CharityProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)

    class Config:
        extra = Extra.forbid


class CharityProjectPatch(CharityProjectCreate):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[int]


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime

    class Config:
        orm_mode = True


class CharityProjectDBPatchDelete(CharityProjectDB):
    close_date: Optional[datetime]
