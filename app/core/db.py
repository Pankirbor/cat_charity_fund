from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Boolean, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class DateTimeMixin:
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, default=None)


class InvestedMixin:
    full_amount = Column(Integer, default=0)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)


class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.db_url)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
