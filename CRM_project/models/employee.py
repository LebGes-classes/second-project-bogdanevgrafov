import datetime

from CRM_project.models.base_person import (
    BasePerson,
)

from dataclasses import (
    dataclass,
)

@dataclass
class Employee(BasePerson):
    """Класс работника."""
    is_hired: bool
    date_of_hire: datetime.date
    workplace: str

    def experience(self):
        """Метод для вывода опыта человека.

        Returns:
            experience: количество лет, месяцев, дней опыта.
        """

        today = datetime.date.today()
        years = today.year - self.date_of_hire.year
        months = today.month - self.date_of_hire.month
        days = today.day - self.date_of_hire.day

        if days < 0:
            months -= 1
            days += 30
        if months < 0:
            years -= 1
            months += 12

        return years, months, days
