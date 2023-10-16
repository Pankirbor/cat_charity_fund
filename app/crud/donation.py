from datetime import datetime
from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDRDonation(CRUDBase):
    pass


donation_crud = CRUDRDonation(Donation)
