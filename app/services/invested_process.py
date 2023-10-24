from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


def recalculation(project: CharityProject, donation: Donation) -> None:
    """Функцая производящая рассчет имеющихся средств
    и обновления объектов фонда и пожертвования"""

    if project.get_balance() >= donation.get_balance():
        project.add_donation(donation.get_balance())
        donation.close_donation()
    else:
        diff = donation.get_balance() - project.get_balance()
        donation.set_new_invested_amount(diff)

    if project.is_amount_collected():
        project.close_project()


async def distribution_of_investments(
    item: Union[CharityProject, Donation], session: AsyncSession
) -> Union[CharityProject, Donation]:
    """Функция распределения средств в фонды."""

    model = Donation if isinstance(item, CharityProject) else CharityProject
    objects = await session.execute(
        select(model).where(model.fully_invested == False)  # noqa
    )
    objects = objects.scalars().all()
    objects.sort(key=lambda x: x.create_date)
    if isinstance(item, Donation):
        for object_ in objects:
            recalculation(object_, item)

    else:
        for object_ in objects:
            recalculation(item, object_)

    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item
