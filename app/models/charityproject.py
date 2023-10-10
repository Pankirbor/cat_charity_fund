from datetime import datetime

from sqlalchemy import Column, String

from app.core.db import Base, DateTimeMixin, InvestedMixin


class CharityProjrct(Base, DateTimeMixin, InvestedMixin):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String, nullable=False)
