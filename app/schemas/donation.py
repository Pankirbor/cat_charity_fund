from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field


class DonationCreate(BaseModel):
    full_amount: int = Field(..., gt=0)
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationDBForUser(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDBAll(DonationDBForUser):
    user_id: Optional[int]
    comment: Optional[str]
    invested_amount: int
    fully_invested: bool = Field(False)
