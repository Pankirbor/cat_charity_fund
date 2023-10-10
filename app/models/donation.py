from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base, DateTimeMixin, InvestedMixin


class Donation(Base, DateTimeMixin, InvestedMixin):
    user_id = (Integer, ForeignKey("user.id"))
    comment = Column(Text)
