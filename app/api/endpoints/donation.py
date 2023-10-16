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
    response_model=list[DonationDBAll],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.post(
    "/",
    response_model=DonationDBForUser,
)
async def create_donation(
    donation_obj: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(
        donation_obj,
        session,
        user,
    )
    new_donation = await distribution_of_investments(new_donation, "donation", session)
    return new_donation


@router.get(
    "/my",
    response_model=list[DonationDBForUser],
    dependencies=[Depends(current_user)],
)
async def get_my_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    donations = await donation_crud.get_by_user(user, session)
    return donations
