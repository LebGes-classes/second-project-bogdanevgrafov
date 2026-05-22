from CRM_project.models.employee import (
    Employee,
)
from dataclasses import (
    dataclass,
)

@dataclass
class WarehouseEmployee(Employee):
    """Класс сотрудника склада."""
    warehouse_id: int

    hours_worked: int
    items_moved: int
    base_salary_on_hour: float = 10

    @property
    def salary(self) -> float:
        """Метод для расчета заработной платы сотрудника склада.

        Returns:
            Зарплата сотрудника склада.
        """

        return self.base_salary_on_hour * self.hours_worked + self.items_moved * 0.5
