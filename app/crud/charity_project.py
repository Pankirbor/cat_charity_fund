from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDRCharityProject(CRUDBase):
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

    async def update_project(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
    ) -> CharityProject:
        """Метод обновления значений объекта,
        расширяющий аналогичный метод базового класса."""

        project = await self.update(db_obj, obj_in, session)
        if project.invested_amount == project.full_amount:
            project.close_project()
            session.add(project)
            await session.commit()
            await session.refresh(project)
        return project


project_crud = CRUDRCharityProject(CharityProject)
