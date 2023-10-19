from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.constans import (
    CLOSE_PROJECT,
    INVALID_DELETE,
    INVALID_FULL_AMOUNT,
    INVALID_NAME_OR_FULL_AMOUNT,
    NAME_DUPLICATE,
    NOT_FOUND_PROJECT,
)
from app.crud.charity_project import project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectPatch


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await project_crud.get_project_id_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail=NAME_DUPLICATE,
        )


async def check_project(
    project_id: int,
    session: AsyncSession,
    msg: str,
) -> CharityProject:
    project = await project_crud.get(project_id, session)
    if not project:
        raise HTTPException(
            status_code=404,
            detail=NOT_FOUND_PROJECT,
        )
    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail=msg,
        )
    return project


async def check_project_before_edit(
    project_id: int,
    obj_in: CharityProjectPatch,
    session: AsyncSession,
) -> CharityProject:
    project = await check_project(project_id, session, CLOSE_PROJECT)

    if obj_in.full_amount:
        if project.invested_amount > obj_in.full_amount:
            raise HTTPException(
                status_code=400,
                detail=INVALID_FULL_AMOUNT,
            )

    for field, value in obj_in.dict().items():
        if value in ("", 0):
            raise HTTPException(
                status_code=422,
                detail=INVALID_NAME_OR_FULL_AMOUNT,
            )

    return project


async def check_project_before_delete(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await check_project(project_id, session, INVALID_DELETE)

    if project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail=INVALID_DELETE,
        )
    return project
