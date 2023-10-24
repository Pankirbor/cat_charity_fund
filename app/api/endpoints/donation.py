from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import (
    DonationCreate,
    DonationDBAll,
    DonationDBForUser,
)
from app.services.invested_process import distribution_of_investments

router = APIRouter()


@router.get(
    "/",
    summary="Список всех пожертвований",
    response_model=list[DonationDBAll],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Получение полного списка пожертвований (**только для администрации**):

    Расшифровка параметров:
    - **full_amount**: количество необходимых средств
    - **comment**: ваш комментарий
    - **id**: уникальный индификатор проекта
    - **create_date**: дата создания
    - **user_id**: уникальный номер пользователя
    - **invested_amount**: количество внесенных средств
    - **fully_invested**: статус проекта (открыт(_False_) или закрыт(_True_))
    """
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.post(
    "/",
    summary="Внести пожертвование",
    response_model=DonationDBForUser,
    response_model_exclude_none=True,
)
async def create_donation(
    donation_obj: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """
    Размещение пожертвования (**только зарегистрированный пользователь**).

    Параметры запроса:
    - **comment**: ваш комментарий (**опционально**)
    - **full_amount**: количество необходимых средств
    """
    new_donation = await donation_crud.create(
        donation_obj,
        session,
        user,
    )
    new_donation = await distribution_of_investments(new_donation, session)
    return new_donation


@router.get(
    "/my",
    summary="Список пожертвований текущего пользователя",
    response_model=list[DonationDBForUser],
    dependencies=[Depends(current_user)],
)
async def get_my_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Получить список своих пожертвований (**только зарегистрированный пользователь**)
    """
    donations = await donation_crud.get_by_user(user, session)
    return donations
