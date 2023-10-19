from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base, DateTimeMixin, InvestedMixin


class Donation(Base, DateTimeMixin, InvestedMixin):
    """
    Класс для работы с объектами 'Пожертвований'.
    """

    comment = Column(Text)
    user_id = Column(Integer, ForeignKey("user.id"))

    def get_balance(self) -> int:
        """
        Метод возвращает размер оставшихся средств для инвестирования.
        """
        return self.full_amount - self.invested_amount

    def set_new_invested_amount(self, value: int) -> None:
        """
        Метод обновляет атрибут 'invested_amount'
        после внесения средств в проект.
        """
        self.invested_amount = self.full_amount - value

    def close_donation(self) -> None:
        """
        Метод осуществляет закрытие пожертвования,
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
