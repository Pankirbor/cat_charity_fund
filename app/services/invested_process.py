from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProjrct, Donation


def recalculation(project: CharityProjrct, donation: Donation) -> None:
    if project.get_balance() >= donation.get_balance():
        project.add_donation(donation.get_balance())
        donation.close_donation()
    else:
        diff = donation.get_balance() - project.get_balance()
        donation.set_new_invested_amount(diff)
        project.close_project()


async def distribution_of_investments(
    item: Union[CharityProjrct, Donation], key: str, session: AsyncSession
) -> Union[CharityProjrct, Donation]:
    models = {"project": Donation, "donation": CharityProjrct}
    objects = await session.execute(
        select(models[key]).where(models[key].fully_invested == bool(False))
    )
    objects = objects.scalars().all()
    objects.sort(key=lambda x: x.create_date)
    if key == "donation":
        for object_ in objects:
            recalculation(object_, item)

    else:
        for object_ in objects:
            recalculation(item, object_)

    await session.commit()
    await session.refresh(item)
    return item
