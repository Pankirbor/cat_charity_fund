from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DonationCreate(BaseModel):
    full_amount: int = Field(..., gt=0)
    comment: Optional[str]


class DonationDBForUser(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDBAll(DonationDBForUser):
    user_id: Optional[int]
    invested_amount: int
    fully_invested: bool = Field(False)
    close_date: Optional[datetime]
