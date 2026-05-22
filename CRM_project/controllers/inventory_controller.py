from CRM_project.models.product import Product
from CRM_project.models.warehouse_cell import WarehouseCell
from CRM_project.repositories.product_repo import ProductRepository
from CRM_project.repositories.sales_point_repo import SalesPointRepository
from CRM_project.repositories.warehouse_repo import WarehouseRepository


class InventoryController:
    """Класс контроллера товаров."""

    def __init__(
        self,
        product_repo: ProductRepository,
        warehouse_repo: WarehouseRepository,
        sales_point_repo: SalesPointRepository,
    ) -> None:
        """Метод инициализации контроллера.

        Args:
            product_repo: репозиторий товаров.
            warehouse_repo: репозиторий складов.
            sales_point_repo: репозиторий пунктов продаж.
        """

        self.product_repo = product_repo
        self.warehouse_repo = warehouse_repo
        self.sales_point_repo = sales_point_repo

    def create_cell(self, warehouse_id: int, cell_id: int, name: str, capacity: int) -> None:
        """Метод создания складской ячейки.

        Args:
            warehouse_id: идентификатор склада.
            cell_id: идентификатор ячейки.
            name: название.
            capacity: емкость.
        """

        warehouse = self._require_warehouse(warehouse_id)
        cell = WarehouseCell(id=cell_id, name=name, capacity=capacity, inventory={})
        warehouse.add_cell(cell)
        self.warehouse_repo.update(warehouse)

    def purchase_product(self, warehouse_id: int, cell_id: int, product_id: int, quantity: int) -> None:
        """Метод закупки товара на склад.

        Args:
            warehouse_id: идентификатор склада.
            cell_id: идентификатор ячейки.
            product_id: идентификатор товара.
            quantity: количество.
        """

        product = self._require_product(product_id)
        if not product.is_available:
            raise ValueError("Товар недоступен к закупке.")
        warehouse = self._require_warehouse(warehouse_id)
        cell = self._require_cell(warehouse, cell_id)
        cell.add(product, quantity)
        self.warehouse_repo.update(warehouse)

    def transfer_between_warehouses(
        self,
        source_warehouse_id: int,
        target_warehouse_id: int,
        product_id: int,
        quantity: int,
        target_cell_id: int,
    ) -> None:
        """Метод перемещения товара между складами.

        Args:
            source_warehouse_id: идентификатор склада-источника.
            target_warehouse_id: идентификатор склада-получателя.
            product_id: идентификатор товара.
            quantity: количество.
            target_cell_id: идентификатор ячейки получателя.
        """

        product = self._require_product(product_id)
        source = self._require_warehouse(source_warehouse_id)
        target = self._require_warehouse(target_warehouse_id)
        source_cell = source.find_cell_by_product(product_id)
        if source_cell is None:
            raise ValueError("Товар не найден на складе.")
        target_cell = self._require_cell(target, target_cell_id)
        source_cell.remove(product, quantity)
        target_cell.add(product, quantity)
        self.warehouse_repo.update(source)
        self.warehouse_repo.update(target)

    def move_to_sales_point(
        self,
        warehouse_id: int,
        sales_point_id: int,
        product_id: int,
        quantity: int,
    ) -> None:
        """Метод перемещения товара со склада в пункт продаж.

        Args:
            warehouse_id: идентификатор склада.
            sales_point_id: идентификатор пункта продаж.
            product_id: идентификатор товара.
            quantity: количество.
        """

        product = self._require_product(product_id)
        warehouse = self._require_warehouse(warehouse_id)
        sales_point = self._require_sales_point(sales_point_id)
        cell = warehouse.find_cell_by_product(product_id)
        if cell is None:
            raise ValueError("Товар не найден на складе.")
        cell.remove(product, quantity)
        sales_point.add(product, quantity)
        self.warehouse_repo.update(warehouse)
        self.sales_point_repo.update(sales_point)

    def return_from_sales_point(
        self,
        sales_point_id: int,
        warehouse_id: int,
        cell_id: int,
        product_id: int,
        quantity: int,
    ) -> None:
        """Метод возврата товара из пункта продаж на склад.

        Args:
            sales_point_id: идентификатор пункта продаж.
            warehouse_id: идентификатор склада.
            cell_id: идентификатор ячейки.
            product_id: идентификатор товара.
            quantity: количество.
        """

        product = self._require_product(product_id)
        sales_point = self._require_sales_point(sales_point_id)
        warehouse = self._require_warehouse(warehouse_id)
        cell = self._require_cell(warehouse, cell_id)
        sales_point.remove(product, quantity)
        cell.add(product, quantity)
        self.sales_point_repo.update(sales_point)
        self.warehouse_repo.update(warehouse)

    def _require_product(self, product_id: int) -> Product:
        product = self.product_repo.get(product_id)
        if product is None:
            raise ValueError("Товар не найден.")
        return product

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

    def _require_cell(self, warehouse, cell_id: int) -> WarehouseCell:
        if cell_id not in warehouse.cells:
            raise ValueError("Ячейка не найдена.")
        return warehouse.cells[cell_id]

