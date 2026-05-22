from CRM_project.models.employee import Employee
from CRM_project.repositories.employee_repo import EmployeeRepository
from CRM_project.repositories.sales_point_repo import SalesPointRepository
from CRM_project.repositories.warehouse_repo import WarehouseRepository


class HrController:
    """Класс контроллера сотрудников."""

    def __init__(
        self,
        employee_repo: EmployeeRepository,
        warehouse_repo: WarehouseRepository,
        sales_point_repo: SalesPointRepository,
    ) -> None:
        """Метод инициализации контроллера.

        Args:
            employee_repo: репозиторий работников.
            warehouse_repo: репозиторий складов.
            sales_point_repo: репозиторий пунктов продаж.
        """

        self.employee_repo = employee_repo
        self.warehouse_repo = warehouse_repo
        self.sales_point_repo = sales_point_repo

    def hire_employee(self, employee: Employee) -> None:
        """Метод найма сотрудника.

        Args:
            employee: сотрудник.
        """

        employee.is_hired = True
        self.employee_repo.add(employee)

    def fire_employee(self, employee_id: int) -> None:
        """Метод увольнения сотрудника.

        Args:
            employee_id: идентификатор сотрудника.
        """

        employee = self._require_employee(employee_id)
        employee.is_hired = False
        self.employee_repo.update(employee)

    def change_responsible(self, node_type: str, node_id: int, employee_id: int) -> None:
        """Метод смены ответственного.

        Args:
            node_type: тип узла (warehouse или sales_point).
            node_id: идентификатор узла.
            employee_id: идентификатор сотрудника.
        """

        self._require_employee(employee_id)
        if node_type == "warehouse":
            warehouse = self._require_warehouse(node_id)
            warehouse.manager_id = employee_id
            self.warehouse_repo.update(warehouse)
            return
        if node_type == "sales_point":
            sales_point = self._require_sales_point(node_id)
            sales_point.manager_id = employee_id
            self.sales_point_repo.update(sales_point)
            return
        raise ValueError("Неизвестный тип узла.")

    def _require_employee(self, employee_id: int):
        employee = self.employee_repo.get(employee_id)
        if employee is None:
            raise ValueError("Сотрудник не найден.")
        return employee

    def _require_warehouse(self, warehouse_id: int):
        warehouse = self.warehouse_repo.get(warehouse_id)
        if warehouse is None:
            raise ValueError("Склад не найден.")
        return warehouse

    def _require_sales_point(self, sales_point_id: int):
        sales_point = self.sales_point_repo.get(sales_point_id)
        if sales_point is None:
            raise ValueError("Пункт продаж не найден.")
        return sales_point

