from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charityproject import project_crud
from app.schemas.charityproject import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectPatch,
)
from app.services.invested_process import distribution_of_investments

router = APIRouter()


@router.get(
    "/",
    response_model=list[CharityProjectDB],
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    all_projects = await project_crud.get_multi(session)
    return all_projects


@router.post(
    "/",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""

    # todo await check_name_duplicate(charity_project.name, session)
    new_project = await project_crud.create(charity_project, session)
    new_project = await distribution_of_investments(new_project, "project", session)
    return new_project


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    # response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectPatch,
    session: AsyncSession = Depends(get_async_session),
):
    pass


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    pass
