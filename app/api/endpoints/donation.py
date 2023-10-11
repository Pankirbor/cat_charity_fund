from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.donation import (
    DonationCreate,
    DonationDBAll,
    DonationDBForUser,
)
from app.core.user import current_user, current_superuser

router = APIRouter()


@router.get(
    "/",
    response_model=list[DonationDBAll],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    pass


@router.post(
    "/",
    response_model=DonationDBForUser,
    dependencies=[Depends(current_user)],
)
async def create_donation(
    donation_obj: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
):
    pass


@router.get(
    "/my",
    response_model=list[DonationDBForUser],
    dependencies=[Depends(current_user)],
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
):
    pass
