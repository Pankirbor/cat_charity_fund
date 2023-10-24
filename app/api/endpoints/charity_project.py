from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_project
from app.constants import CLOSE_PROJECT, INVALID_DELETE
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import project_crud
from app.exceptions import DuplicateNameException
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectPatch,
    CharityProjectDBPatchDelete,
)
from app.services.invested_process import distribution_of_investments

router = APIRouter()


@router.get(
    "/",
    summary="Список всех проектов фонда",
    response_model=list[CharityProjectDB],
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Получение полного списка фондов для всех пользователей:

    - **name**: название проекта
    - **description**: цель проекта
    - **full_amount**: количество необходимых средств
    - **id**: уникальный индификатор проекта
    - **invested_amount**: количество внесенных средств
    - **fully_invested**: статус проекта (открыт(_False_) или закрыт(_True_))
    - **create_date**: дата создания
    """
    all_projects = await project_crud.get_multi(session)
    return all_projects


@router.post(
    "/",
    summary="Открыть новый проект",
    response_model=CharityProjectDBPatchDelete,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Открытие нового проекта (**только для администрации**).

    Обязательные параметры запроса:
    - **name**: название проекта
    - **description**: цель проекта
    - **full_amount**: количество необходимых средств

    """

    try:
        new_project = await project_crud.create_project(charity_project, session)
        new_project = await distribution_of_investments(new_project, "project", session)
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=str(err),
        )

    return new_project


@router.patch(
    "/{project_id}",
    summary="Редактировать проект",
    response_model=CharityProjectDBPatchDelete,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectPatch,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Изменить существующий проект (**только для администрации**):
    - можно изменять название и описание существующего проекта,
    - устанавливать для него новую требуемую сумму (**но не меньше уже внесённой**).
    - нельзя модифицировать закрытые проекты, изменять даты создания и закрытия проектов.

    Обязательный path-параметр:
    - **id**: уникальный номер проекта
    """

    project = await check_project(project_id, session, CLOSE_PROJECT)
    try:
        project = await project_crud.update_project(project, obj_in, session)
    except DuplicateNameException as err:
        raise HTTPException(
            status_code=400,
            detail=str(err),
        )
    except Exception as err:
        raise HTTPException(
            status_code=422,
            detail=str(err),
        )
    return project


@router.delete(
    "/{project_id}",
    summary="Удалить проект",
    response_model=CharityProjectDBPatchDelete,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Удалить существующий проект (**только для администрации**):
    - можно удалить проекты, в которые не было внесено средств,
    - закрытые проекты удалять нельзя.

    Обязательный path-параметр:
    - **id**: уникальный номер проекта
    """

    project = await check_project(project_id, session, INVALID_DELETE)
    try:
        project = await project_crud.remove_project(project, session)
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=str(err),
        )
    return project
