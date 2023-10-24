from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import INVALID_DELETE, INVALID_FULL_AMOUNT, NAME_DUPLICATE
from app.crud.base import CRUDBase
from app.exceptions import (
    DuplicateNameException,
    InvalidDeleteException,
    InvalidPatchException,
)
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectCreate, CharityProjectPatch


class CRUDRCharityProject(CRUDBase):
    """Класс для работы с объектами таблицы CharityProject"""

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        """Метод для получения id объекта таблицы по названию."""

        db_project_id = await session.execute(
            select(CharityProject.id).where(CharityProject.name == project_name)
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def check_name_duplicate(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> None:
        """Метод проверки на уникальность названия проекта."""

        project_id = await self.get_project_id_by_name(project_name, session)
        if project_id:
            raise DuplicateNameException(NAME_DUPLICATE)

    async def create_project(
        self,
        obj_in: CharityProjectCreate,
        session: AsyncSession,
    ) -> CharityProject:
        """Метод создания проекта,
        расширяющий аналогичный метод базового класса."""

        await self.check_name_duplicate(obj_in.name, session)
        project = await self.create(obj_in, session)

        return project

    async def update_project(
        self,
        db_obj: CharityProject,
        obj_in: CharityProjectPatch,
        session: AsyncSession,
    ) -> CharityProject:
        """Метод обновления значений проекта,
        расширяющий аналогичный метод базового класса."""

        await self.check_name_duplicate(obj_in.name, session)
        if obj_in.full_amount:
            if db_obj.invested_amount > obj_in.full_amount:
                raise InvalidPatchException(INVALID_FULL_AMOUNT)

        project = await self.update(db_obj, obj_in, session)
        if project.invested_amount == project.full_amount:
            project.close_project()
            session.add(project)
            await session.commit()
            await session.refresh(project)
        return project

    async def remove_project(
        self,
        db_obj: CharityProject,
        session: AsyncSession,
    ) -> CharityProject:
        """Метод удаления проекта,
        расширяющий аналогичный метод базового класса."""

        if db_obj.invested_amount:
            raise InvalidDeleteException(INVALID_DELETE)

        project = await self.remove(db_obj, session)
        return project


project_crud = CRUDRCharityProject(CharityProject)
