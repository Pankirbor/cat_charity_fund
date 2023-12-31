from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.constants import DEFAULT_AMOUNT
from app.core.config import settings


class DateTimeMixin:
    """
    Миксин для добавления в таблицу полей дат.
    """

    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, default=None)


class InvestedMixin:
    """
    Миксин для добавления в таблицу полей отслеживания инвестиций.
    """

    full_amount = Column(Integer, default=DEFAULT_AMOUNT)
    invested_amount = Column(Integer, default=DEFAULT_AMOUNT)
    fully_invested = Column(Boolean, default=False)


class PreBase:
    """
    Класс, расширяющий базовую таблицу.
    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.db_url)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    """Генератор асинхронных сессий"""

    async with AsyncSessionLocal() as async_session:
        yield async_session
