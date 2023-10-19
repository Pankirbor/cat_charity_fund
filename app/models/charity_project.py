from datetime import datetime

from sqlalchemy import Column, String

from app.core.db import Base, DateTimeMixin, InvestedMixin


class CharityProject(Base, DateTimeMixin, InvestedMixin):
    """
    Класс для работы с объектами Благотворительных фондов.
    """

    name = Column(String(100), unique=True, nullable=False)
    description = Column(String, nullable=False)

    def is_amount_collected(self):
        """
        Метод проверяющий выполнение цели по сбору средств проекта.
        """
        return self.invested_amount == self.full_amount

    def get_balance(self) -> int:
        """
        Метод возвращает размер недостающих средств до выполнения цели.
        """
        return self.full_amount - self.invested_amount

    def add_donation(self, amount: int) -> None:
        """
        Метод добавляет внесенную сумму пожертвования и обновляет
        и обновляет атрибут 'invested_amount.'
        """
        self.invested_amount = self.invested_amount + amount

    def close_project(self) -> None:
        """
        Метод осуществляет закрытие проекта,
        устанавлиявая соответствующие значения атрибутам.
        """
        self.close_date = datetime.utcnow()
        self.invested_amount = self.full_amount
        self.fully_invested = True

    def __repr__(self) -> str:
        """
        Метод представления объекта.
        """
        return f"{self.name}: {self.created_date} - {self.close_date}"
