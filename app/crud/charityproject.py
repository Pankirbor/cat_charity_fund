from datetime import datetime
from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProjrct, User


class CRUDRCharityProjrct(CRUDBase):
    pass


project_crud = CRUDRCharityProjrct(CharityProjrct)
