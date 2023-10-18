from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectPatch

"""
Суперпользователь может:
создавать проекты,
удалять проекты, в которые не было внесено средств,
изменять название и описание существующего проекта,
устанавливать для него новую требуемую сумму (но не меньше уже внесённой).

Никто не может менять через API размер внесённых средств,
удалять или модифицировать закрытые проекты,
изменять даты создания и закрытия проектов.
"""


# todo сделать валидатор для проверки
async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await project_crud.get_project_id_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail="Проект с таким именем уже существует!",
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
            detail="Проект не найден!",
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
    project = await check_project(
        project_id, session, "Закрытый проект нельзя редактировать!"
    )

    if obj_in.full_amount:
        if project.invested_amount > obj_in.full_amount:
            raise HTTPException(
                status_code=400,
                detail="Невозможно устанавить новую требуемую сумму, так как она меньше уже собранной.",
            )

    for field, value in obj_in.dict().items():
        if value in ("", 0):
            raise HTTPException(
                status_code=422,
                detail="имя или оптсание не может быть пустой строкой или None",
            )

    return project


async def check_project_before_delete(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await check_project(
        project_id, session, "В проект были внесены средства, не подлежит удалению!"
    )

    if project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail="В проект были внесены средства, не подлежит удалению!",
        )
    return project
