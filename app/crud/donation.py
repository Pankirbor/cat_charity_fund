from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDRDonation(CRUDBase):
    """Класс для работы с объектами таблицы Donation"""

    async def get_by_user(
        self,
        user: User,
        session: AsyncSession,
    ) -> list[Donation]:
        """Метод для получения всех пожертвований с конкретным user_id."""

        donations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return donations.scalars().all()


donation_crud = CRUDRDonation(Donation)
