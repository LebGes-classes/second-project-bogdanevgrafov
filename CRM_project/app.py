import datetime
import os

from CRM_project.controllers.hr_controller import HrController
from CRM_project.controllers.inventory_controller import InventoryController
from CRM_project.controllers.logistics_controller import LogisticsController
from CRM_project.controllers.reports_controller import ReportsController
from CRM_project.controllers.sales_controller import SalesController
from CRM_project.models.base_person import Gender
from CRM_project.models.sales_point_employee import SalesPointEmployee
from CRM_project.models.warehouse_employee import WarehouseEmployee
from CRM_project.repositories.customer_repo import CustomerRepository
from CRM_project.repositories.employee_repo import EmployeeRepository
from CRM_project.repositories.order_repo import OrderRepository
from CRM_project.repositories.product_repo import ProductRepository
from CRM_project.repositories.sales_point_repo import SalesPointRepository
from CRM_project.repositories.warehouse_repo import WarehouseRepository
from CRM_project.views.forms import input_date, input_int, input_str
from CRM_project.views.menu import choose, show_error, show_message
from CRM_project.views.printer import print_inventory, print_kv


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


class CrmApp:
    """Класс приложения CRM."""

    def __init__(self) -> None:
        """Метод инициализации приложения."""

        product_repo = ProductRepository(os.path.join(DATA_DIR, "products.json"))
        warehouse_repo = WarehouseRepository(os.path.join(DATA_DIR, "warehouses.json"))
        sales_point_repo = SalesPointRepository(os.path.join(DATA_DIR, "sales_points.json"))
        employee_repo = EmployeeRepository(os.path.join(DATA_DIR, "employees.json"))
        customer_repo = CustomerRepository(os.path.join(DATA_DIR, "customers.json"))
        order_repo = OrderRepository(os.path.join(DATA_DIR, "orders.json"))

        self.inventory_controller = InventoryController(product_repo, warehouse_repo, sales_point_repo)
        self.logistics_controller = LogisticsController(warehouse_repo, sales_point_repo)
        self.hr_controller = HrController(employee_repo, warehouse_repo, sales_point_repo)
        self.sales_controller = SalesController(product_repo, sales_point_repo, order_repo, customer_repo)
        self.reports_controller = ReportsController(product_repo, warehouse_repo, sales_point_repo, order_repo)

        self.product_repo = product_repo
        self.customer_repo = customer_repo
        self.employee_repo = employee_repo
        self.warehouse_repo = warehouse_repo
        self.sales_point_repo = sales_point_repo

    def run(self) -> None:
        """Метод запуска приложения."""

        while True:
            choice = choose(
                "Главное меню",
                [
                    "Склады",
                    "Пункты продаж",
                    "Товары и логистика",
                    "Сотрудники",
                    "Продажи и возвраты",
                    "Отчеты",
                    "Выход",
                ],
                allow_zero=False,
            )
            try:
                if choice == 1:
                    self._warehouses_menu()
                elif choice == 2:
                    self._sales_points_menu()
                elif choice == 3:
                    self._inventory_menu()
                elif choice == 4:
                    self._hr_menu()
                elif choice == 5:
                    self._sales_menu()
                elif choice == 6:
                    self._reports_menu()
                elif choice == 7:
                    show_message("Выход из программы.")
                    return
            except ValueError as exc:
                show_error(str(exc))

    def _warehouses_menu(self) -> None:
        while True:
            choice = choose(
                "Склады",
                [
                    "Открыть склад",
                    "Закрыть склад",
                    "Информация о складе",
                    "Создать ячейку",
                    "Смена ответственного",
                ],
            )
            if choice == 0:
                return
            if choice == 1:
                self._open_warehouse()
            elif choice == 2:
                warehouse_id = input_int("ID склада: ")
                self.logistics_controller.close_warehouse(warehouse_id)
                show_message("Склад закрыт.")
            elif choice == 3:
                warehouse_id = input_int("ID склада: ")
                info = self.reports_controller.warehouse_info(warehouse_id)
                print_kv("Информация о складе", info)
            elif choice == 4:
                warehouse_id = input_int("ID склада: ")
                name = input_str("Название ячейки: ")
                capacity = input_int("Емкость: ")
                warehouse = self._require_warehouse(warehouse_id)
                cell_id = self._next_cell_id(warehouse)
                self.inventory_controller.create_cell(warehouse_id, cell_id, name, capacity)
                show_message(f"Ячейка создана. ID: {cell_id}")
            elif choice == 5:
                warehouse_id = input_int("ID склада: ")
                employee_id = input_int("ID сотрудника: ")
                self.hr_controller.change_responsible("warehouse", warehouse_id, employee_id)
                show_message("Ответственный назначен.")

    def _open_warehouse(self) -> None:
        warehouse_id = self._next_id(self.warehouse_repo.list())
        city = input_str("Город: ")
        address = input_str("Адрес: ")
        name = input_str("Название: ")
        self.logistics_controller.open_warehouse(warehouse_id, city, address, name)
        show_message(f"Склад открыт. ID: {warehouse_id}")

    def _sales_points_menu(self) -> None:
        while True:
            choice = choose(
                "Пункты продаж",
                [
                    "Открыть пункт продаж",
                    "Закрыть пункт продаж",
                    "Информация о пункте продаж",
                    "Смена ответственного",
                ],
            )
            if choice == 0:
                return
            if choice == 1:
                self._open_sales_point()
            elif choice == 2:
                sales_point_id = input_int("ID пункта продаж: ")
                self.logistics_controller.close_sales_point(sales_point_id)
                show_message("Пункт продаж закрыт.")
            elif choice == 3:
                sales_point_id = input_int("ID пункта продаж: ")
                info = self.reports_controller.sales_point_info(sales_point_id)
                print_kv("Информация о пункте продаж", info)
            elif choice == 4:
                sales_point_id = input_int("ID пункта продаж: ")
                employee_id = input_int("ID сотрудника: ")
                self.hr_controller.change_responsible("sales_point", sales_point_id, employee_id)
                show_message("Ответственный назначен.")

    def _open_sales_point(self) -> None:
        sales_point_id = self._next_id(self.sales_point_repo.list())
        city = input_str("Город: ")
        address = input_str("Адрес: ")
        name = input_str("Название: ")
        self.logistics_controller.open_sales_point(sales_point_id, city, address, name)
        show_message(f"Пункт продаж открыт. ID: {sales_point_id}")

    def _inventory_menu(self) -> None:
        while True:
            choice = choose(
                "Товары и логистика",
                [
                    "Закупка товара",
                    "Перемещение между складами",
                    "Перемещение на пункт продаж",
                    "Возврат с пункта продаж",
                ],
            )
            if choice == 0:
                return
            if choice == 1:
                warehouse_id = input_int("ID склада: ")
                cell_id = input_int("ID ячейки: ")
                product_id = input_int("ID товара: ")
                quantity = input_int("Количество: ")
                self.inventory_controller.purchase_product(warehouse_id, cell_id, product_id, quantity)
                show_message("Товар закуплен.")
            elif choice == 2:
                source_id = input_int("ID склада-источника: ")
                target_id = input_int("ID склада-получателя: ")
                product_id = input_int("ID товара: ")
                quantity = input_int("Количество: ")
                target_cell_id = input_int("ID ячейки получателя: ")
                self.inventory_controller.transfer_between_warehouses(
                    source_id,
                    target_id,
                    product_id,
                    quantity,
                    target_cell_id,
                )
                show_message("Товар перемещен.")
            elif choice == 3:
                warehouse_id = input_int("ID склада: ")
                sales_point_id = input_int("ID пункта продаж: ")
                product_id = input_int("ID товара: ")
                quantity = input_int("Количество: ")
                self.inventory_controller.move_to_sales_point(
                    warehouse_id,
                    sales_point_id,
                    product_id,
                    quantity,
                )
                show_message("Товар отправлен в пункт продаж.")
            elif choice == 4:
                sales_point_id = input_int("ID пункта продаж: ")
                warehouse_id = input_int("ID склада: ")
                cell_id = input_int("ID ячейки: ")
                product_id = input_int("ID товара: ")
                quantity = input_int("Количество: ")
                self.inventory_controller.return_from_sales_point(
                    sales_point_id,
                    warehouse_id,
                    cell_id,
                    product_id,
                    quantity,
                )
                show_message("Товар возвращен на склад.")

    def _hr_menu(self) -> None:
        while True:
            choice = choose(
                "Сотрудники",
                [
                    "Нанять сотрудника склада",
                    "Нанять сотрудника пункта продаж",
                    "Уволить сотрудника",
                ],
            )
            if choice == 0:
                return
            if choice == 1:
                employee = self._create_warehouse_employee()
                self.hr_controller.hire_employee(employee)
                show_message("Сотрудник нанят.")
            elif choice == 2:
                employee = self._create_sales_employee()
                self.hr_controller.hire_employee(employee)
                show_message("Сотрудник нанят.")
            elif choice == 3:
                employee_id = input_int("ID сотрудника: ")
                self.hr_controller.fire_employee(employee_id)
                show_message("Сотрудник уволен.")

    def _create_warehouse_employee(self) -> WarehouseEmployee:
        employee_id = self._next_id(self.employee_repo.list())
        first_name = input_str("Имя: ")
        second_name = input_str("Фамилия: ")
        date_of_birth = input_date("Дата рождения")
        sex = self._choose_gender()
        phone_number = input_str("Телефон: ")
        email = input_str("Email: ")
        password = input_str("Пароль: ")
        country = input_str("Страна: ")
        city = input_str("Город: ")
        address = input_str("Адрес: ")
        warehouse_id = input_int("ID склада: ")
        return WarehouseEmployee(
            id=employee_id,
            first_name=first_name,
            second_name=second_name,
            date_of_birth=date_of_birth,
            sex=sex,
            phone_number=phone_number,
            email=email,
            password=password,
            country=country,
            city=city,
            address=address,
            is_hired=True,
            date_of_hire=datetime.date.today(),
            workplace="Склад",
            warehouse_id=warehouse_id,
            hours_worked=0,
            items_moved=0,
        )

    def _create_sales_employee(self) -> SalesPointEmployee:
        employee_id = self._next_id(self.employee_repo.list())
        first_name = input_str("Имя: ")
        second_name = input_str("Фамилия: ")
        date_of_birth = input_date("Дата рождения")
        sex = self._choose_gender()
        phone_number = input_str("Телефон: ")
        email = input_str("Email: ")
        password = input_str("Пароль: ")
        country = input_str("Страна: ")
        city = input_str("Город: ")
        address = input_str("Адрес: ")
        sales_point_id = input_int("ID пункта продаж: ")
        return SalesPointEmployee(
            id=employee_id,
            first_name=first_name,
            second_name=second_name,
            date_of_birth=date_of_birth,
            sex=sex,
            phone_number=phone_number,
            email=email,
            password=password,
            country=country,
            city=city,
            address=address,
            is_hired=True,
            date_of_hire=datetime.date.today(),
            workplace="Пункт продаж",
            sales_point_id=sales_point_id,
            total_sales_count=0,
            total_sales_amount=0.0,
        )

    def _choose_gender(self) -> Gender:
        choice = choose("Пол", ["Мужской", "Женский", "Другое"], allow_zero=False)
        if choice == 1:
            return Gender.MALE
        if choice == 2:
            return Gender.FEMALE
        return Gender.OTHER

    def _sales_menu(self) -> None:
        while True:
            choice = choose(
                "Продажи и возвраты",
                [
                    "Продать товар",
                    "Возврат заказа",
                ],
            )
            if choice == 0:
                return
            if choice == 1:
                sales_point_id = input_int("ID пункта продаж: ")
                product_id = input_int("ID товара: ")
                quantity = input_int("Количество: ")
                customer_id = input_int("ID покупателя: ")
                self.sales_controller.sell_product(sales_point_id, product_id, quantity, customer_id)
                show_message("Продажа выполнена.")
            elif choice == 2:
                order_id = input_int("ID заказа: ")
                self.sales_controller.return_order(order_id)
                show_message("Возврат выполнен.")

    def _reports_menu(self) -> None:
        while True:
            choice = choose(
                "Отчеты",
                [
                    "Информация о складе",
                    "Информация о пункте продаж",
                    "Товары на складе",
                    "Товары в пункте продаж",
                    "Товары доступные к закупке",
                    "Доходность пункта продаж",
                    "Доходность предприятия",
                ],
            )
            if choice == 0:
                return
            if choice == 1:
                warehouse_id = input_int("ID склада: ")
                info = self.reports_controller.warehouse_info(warehouse_id)
                print_kv("Информация о складе", info)
            elif choice == 2:
                sales_point_id = input_int("ID пункта продаж: ")
                info = self.reports_controller.sales_point_info(sales_point_id)
                print_kv("Информация о пункте продаж", info)
            elif choice == 3:
                warehouse_id = input_int("ID склада: ")
                inventory = self.reports_controller.warehouse_inventory(warehouse_id)
                products = {product.id: product for product in self.product_repo.list()}
                print_inventory("Товары на складе", inventory, products)
            elif choice == 4:
                sales_point_id = input_int("ID пункта продаж: ")
                inventory = self.reports_controller.sales_point_inventory(sales_point_id)
                products = {product.id: product for product in self.product_repo.list()}
                print_inventory("Товары в пункте продаж", inventory, products)
            elif choice == 5:
                available = self.reports_controller.available_products()
                if not available:
                    show_message("Нет доступных товаров.")
                else:
                    for product in available:
                        print(f"{product.id} | {product.name} | {product.price}")
            elif choice == 6:
                sales_point_id = input_int("ID пункта продаж: ")
                profit = self.reports_controller.profit_for_sales_point(sales_point_id)
                show_message(f"Доходность пункта продаж: {profit}")
            elif choice == 7:
                profit = self.reports_controller.total_profit()
                show_message(f"Доходность предприятия: {profit}")

    def _next_id(self, items: list) -> int:
        """Метод получения следующего ID.

        Args:
            items: список объектов с полем id.

        Returns:
            Следующий ID.
        """

        return max((item.id for item in items), default=0) + 1

    def _next_cell_id(self, warehouse) -> int:
        """Метод получения следующего ID ячейки.

        Args:
            warehouse: склад.

        Returns:
            Следующий ID ячейки.
        """

        return max(warehouse.cells.keys(), default=0) + 1

    def _require_warehouse(self, warehouse_id: int):
        warehouse = self.warehouse_repo.get(warehouse_id)
        if warehouse is None:
            raise ValueError("Склад не найден.")
        return warehouse


if __name__ == "__main__":
    app = CrmApp()
    app.run()

