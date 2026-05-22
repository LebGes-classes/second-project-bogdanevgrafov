from CRM_project.models.employee import Employee
from CRM_project.models.sales_point_employee import SalesPointEmployee
from CRM_project.models.warehouse_employee import WarehouseEmployee
from CRM_project.models.base_person import Gender
from CRM_project.repositories.base_repository import BaseRepository
from CRM_project.utils.serialization import format_date, parse_date


class EmployeeRepository(BaseRepository):
    """Класс репозитория работников."""

    def list(self) -> list[Employee]:
        """Метод получения списка работников.

        Returns:
            Список работников.
        """

        return [self._from_dict(item) for item in self._read()]

    def get(self, employee_id: int) -> Employee | None:
        """Метод получения работника по ID.

        Args:
            employee_id: идентификатор работника.

        Returns:
            Работник или None.
        """

        for item in self.list():
            if item.id == employee_id:
                return item
        return None

    def add(self, employee: Employee) -> None:
        """Метод добавления работника.

        Args:
            employee: работник.
        """

        items = self.list()
        if any(existing.id == employee.id for existing in items):
            raise ValueError("Работник с таким ID уже существует.")
        items.append(employee)
        self._write([self._to_dict(item) for item in items])

    def update(self, employee: Employee) -> None:
        """Метод обновления работника.

        Args:
            employee: работник.
        """

        items = self.list()
        updated = False
        for index, item in enumerate(items):
            if item.id == employee.id:
                items[index] = employee
                updated = True
                break
        if not updated:
            raise ValueError("Работник не найден.")
        self._write([self._to_dict(item) for item in items])

    def _from_dict(self, data: dict) -> Employee:
        base_fields = {
            "id": int(data["id"]),
            "first_name": data["first_name"],
            "second_name": data["second_name"],
            "date_of_birth": parse_date(data["date_of_birth"]),
            "sex": Gender(data["sex"]),
            "phone_number": data["phone_number"],
            "email": data["email"],
            "password": data["password"],
            "country": data["country"],
            "city": data["city"],
            "address": data["address"],
            "is_hired": bool(data["is_hired"]),
            "date_of_hire": parse_date(data["date_of_hire"]),
            "workplace": data["workplace"],
        }
        if data.get("employee_type") == "warehouse":
            return WarehouseEmployee(
                **base_fields,
                warehouse_id=int(data["warehouse_id"]),
                hours_worked=int(data.get("hours_worked", 0)),
                items_moved=int(data.get("items_moved", 0)),
                base_salary_on_hour=float(data.get("base_salary_on_hour", 10)),
            )
        if data.get("employee_type") == "sales":
            return SalesPointEmployee(
                **base_fields,
                sales_point_id=int(data["sales_point_id"]),
                total_sales_count=int(data.get("total_sales_count", 0)),
                total_sales_amount=float(data.get("total_sales_amount", 0.0)),
                base_salary_on_month=float(data.get("base_salary_on_month", 1500)),
            )
        raise ValueError("Неизвестный тип работника.")

    def _to_dict(self, employee: Employee) -> dict:
        base = {
            "id": employee.id,
            "first_name": employee.first_name,
            "second_name": employee.second_name,
            "date_of_birth": format_date(employee.date_of_birth),
            "sex": employee.sex.value,
            "phone_number": employee.phone_number,
            "email": employee.email,
            "password": employee.password,
            "country": employee.country,
            "city": employee.city,
            "address": employee.address,
            "is_hired": employee.is_hired,
            "date_of_hire": format_date(employee.date_of_hire),
            "workplace": employee.workplace,
        }
        if isinstance(employee, WarehouseEmployee):
            return {
                **base,
                "employee_type": "warehouse",
                "warehouse_id": employee.warehouse_id,
                "hours_worked": employee.hours_worked,
                "items_moved": employee.items_moved,
                "base_salary_on_hour": employee.base_salary_on_hour,
            }
        if isinstance(employee, SalesPointEmployee):
            return {
                **base,
                "employee_type": "sales",
                "sales_point_id": employee.sales_point_id,
                "total_sales_count": employee.total_sales_count,
                "total_sales_amount": employee.total_sales_amount,
                "base_salary_on_month": employee.base_salary_on_month,
            }
        raise ValueError("Неизвестный тип работника.")

