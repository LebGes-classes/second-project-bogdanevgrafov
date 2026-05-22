from CRM_project.models.base_person import (
    BasePerson,
)
from dataclasses import (
    dataclass,
)

@dataclass
class Customer(BasePerson):
    """Класс покупателя."""
    order_list: list

    @property
    def is_adult(self) -> bool:
        """Метод для определения статуса совершеннолетия.

        Returns:
            Статус (совершеннолетний/несовершеннолетний).
        """

        return self.age >= 18
