from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base, DateTimeMixin, InvestedMixin


class Donation(Base, DateTimeMixin, InvestedMixin):
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey("user.id"))

    def get_balance(self):
        return self.full_amount - self.invested_amount

    def set_new_invested_amount(self, value):
        self.invested_amount = self.full_amount - value

    def close_donation(self):
        self.close_date = datetime.utcnow()
        self.invested_amount = self.full_amount
        self.fully_invested = True

    def __repr__(self):
        return f"{self.name}: {self.created_date} - {self.close_date}"
