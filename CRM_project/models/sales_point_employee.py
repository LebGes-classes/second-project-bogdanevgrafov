from CRM_project.models.employee import (
    Employee,
)
from dataclasses import (
    dataclass,
)

@dataclass
class SalesPointEmployee(Employee):
    """Класс сотрудника пункта продаж."""
    sales_point_id: int

    total_sales_count: int
    total_sales_amount: float
    base_salary_on_month: float = 1500

    @property
    def salary(self) -> float:
        """Метод для расчета заработной платы сотрудника торговой точки.

        Returns:
            Зарплата сотрудника торговой точки.
        """

        return self.base_salary_on_month + self.total_sales_amount * 0.05
    