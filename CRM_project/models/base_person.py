from dataclasses import dataclass
import datetime
from enum import Enum


class Gender(Enum):
    """Класс для определения пола человека."""

    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'


@dataclass
class BasePerson:
    """Базовый класс человека."""

    id: int

    first_name: str
    second_name: str
    date_of_birth: datetime.date
    sex: Gender

    phone_number: str
    email: str
    password: str

    country: str
    city: str
    address: str

    @property
    def age(self) -> int:
        """Метод получения возраста.

        Returns:
            age: Количество полных лет.
        """

        today = datetime.date.today()
        age = today.year - self.date_of_birth.year

        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1

        return age

    @property
    def full_address(self) -> str:
        """Метод получения полного адреса.

        Returns:
            Полный адрес (страна, город, адрес).
        """

        return f'{self.country}, {self.city}, {self.address}'
