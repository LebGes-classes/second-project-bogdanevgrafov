from CRM_project.models.order import OrderStatus
from CRM_project.repositories.order_repo import OrderRepository
from CRM_project.repositories.product_repo import ProductRepository
from CRM_project.repositories.sales_point_repo import SalesPointRepository
from CRM_project.repositories.warehouse_repo import WarehouseRepository


class ReportsController:
    """Класс контроллера отчетов."""

    def __init__(
        self,
        product_repo: ProductRepository,
        warehouse_repo: WarehouseRepository,
        sales_point_repo: SalesPointRepository,
        order_repo: OrderRepository,
    ) -> None:
        """Метод инициализации контроллера.

        Args:
            product_repo: репозиторий товаров.
            warehouse_repo: репозиторий складов.
            sales_point_repo: репозиторий пунктов продаж.
            order_repo: репозиторий заказов.
        """

        self.product_repo = product_repo
        self.warehouse_repo = warehouse_repo
        self.sales_point_repo = sales_point_repo
        self.order_repo = order_repo

    def warehouse_info(self, warehouse_id: int) -> dict:
        """Метод получения информации о складе.

        Args:
            warehouse_id: идентификатор склада.

        Returns:
            Словарь с данными.
        """

        warehouse = self._require_warehouse(warehouse_id)
        return {
            "id": warehouse.id,
            "name": warehouse.name,
            "status": warehouse.status.value,
            "cells": warehouse.number_of_cells,
            "capacity": warehouse.total_capacity,
            "manager_id": warehouse.manager_id,
        }

    def sales_point_info(self, sales_point_id: int) -> dict:
        """Метод получения информации о пункте продаж.

        Args:
            sales_point_id: идентификатор пункта продаж.

        Returns:
            Словарь с данными.
        """

        sales_point = self._require_sales_point(sales_point_id)
        return {
            "id": sales_point.id,
            "name": sales_point.name,
            "status": sales_point.status.value,
            "items_count": sum(sales_point.inventory.values()),
            "manager_id": sales_point.manager_id,
        }

    def warehouse_inventory(self, warehouse_id: int) -> dict[int, int]:
        """Метод получения товаров на складе.

        Args:
            warehouse_id: идентификатор склада.

        Returns:
            Словарь товара и количества.
        """

        warehouse = self._require_warehouse(warehouse_id)
        result: dict[int, int] = {}
        for cell in warehouse.cells.values():
            for product_id, quantity in cell.inventory.items():
                result[product_id] = result.get(product_id, 0) + quantity
        return result

    def sales_point_inventory(self, sales_point_id: int) -> dict[int, int]:
        """Метод получения товаров в пункте продаж.

        Args:
            sales_point_id: идентификатор пункта продаж.

        Returns:
            Словарь товара и количества.
        """

        sales_point = self._require_sales_point(sales_point_id)
        return sales_point.inventory

    def available_products(self) -> list:
        """Метод получения товаров доступных к закупке.

        Returns:
            Список товаров.
        """

        return [product for product in self.product_repo.list() if product.is_available]

    def profit_for_sales_point(self, sales_point_id: int) -> float:
        """Метод получения доходности пункта продаж.

        Args:
            sales_point_id: идентификатор пункта продаж.

        Returns:
            Доходность.
        """

        profit = 0.0
        for order in self.order_repo.list():
            if order.sales_point_id != sales_point_id:
                continue
            if order.status == OrderStatus.SOLD:
                profit += order.total_amount
            else:
                profit -= order.total_amount
        return profit

    def total_profit(self) -> float:
        """Метод получения доходности предприятия.

        Returns:
            Доходность.
        """

        profit = 0.0
        for order in self.order_repo.list():
            if order.status == OrderStatus.SOLD:
                profit += order.total_amount
            else:
                profit -= order.total_amount
        return profit

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

