from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import NOT_FOUND_PROJECT
from app.crud.charity_project import project_crud
from app.models import CharityProject


async def is_object_exists(
    project_id: int,
    session: AsyncSession,
    msg: str,
) -> CharityProject:
    """Функция проверяющая наличие проекта в базе данных"""

    project = await project_crud.get(project_id, session)
    if not project:
        raise HTTPException(
            status_code=404,
            detail=NOT_FOUND_PROJECT,
        )

    return project
