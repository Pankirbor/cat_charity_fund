from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:
    """
    Базовый класс для работы с объектами таблиц
    и выполнения основных операций CRUD.
    """

    def __init__(self, model):
        """Инициилизатор таблицы."""
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ):
        """Метод получения объекта по id из таблицы."""

        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_multi(self, session: AsyncSession):
        """Метод получения всех объектов из таблицы."""

        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[User] = None,
    ):
        """Метод для создания объекта в таблице"""

        obj_in_data = obj_in.dict()
        if user is not None:
            user_id = user.id
            obj_in_data["user_id"] = user_id

        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
    ):
        """Метод для обновления значений объекта в таблице."""

        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj,
        session: AsyncSession,
    ):
        """Метод удаления объекта из таблицы."""

        await session.delete(db_obj)
        await session.commit()
        return db_obj
