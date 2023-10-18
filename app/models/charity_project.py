from datetime import datetime

from sqlalchemy import Column, String

from app.core.db import Base, DateTimeMixin, InvestedMixin


class CharityProject(Base, DateTimeMixin, InvestedMixin):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String, nullable=False)

    def is_amount_collected(self):
        return self.invested_amount == self.full_amount

    def get_balance(self):
        return self.full_amount - self.invested_amount

    def add_donation(self, amount):
        self.invested_amount = self.invested_amount + amount

    def close_project(self):
        self.close_date = datetime.utcnow()
        self.invested_amount = self.full_amount
        self.fully_invested = True

    def __repr__(self):
        return f"{self.name}: {self.created_date} - {self.close_date}"
