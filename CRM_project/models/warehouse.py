import enum
from dataclasses import dataclass

from CRM_project.models.logistics_node import LogisticsNode
from CRM_project.models.warehouse_cell import WarehouseCell

@dataclass
class Warehouse(LogisticsNode):
    """Класс склада."""
    cells: dict[int, WarehouseCell]

    def add_cell(self, cell: WarehouseCell):
        """Метод добавления новой ячейки.

        Args:
            cell: Складская ячейка.
        """

        if cell.id in self.cells:
            raise ValueError("Ячейка с таким ID уже существует в складе.")
        self.cells[cell.id] = cell

    def remove_cell(self, cell: WarehouseCell):
        """Метод удаления ячейки.

        Args:
            cell: Складская ячейка.
        """

        if cell.id in self.cells:
            del self.cells[cell.id]
        else:
            raise ValueError("Ячейки с таким ID нет на складе!")

    def find_cell_by_product(self, product_id: int) -> WarehouseCell | None:
        """Метод для поиска ячейки по ID продукта.

        Args:
            product_id: ID продукта, который нужно найти.

        Returns:
            Ячейка, в которой находится продукт, или None, если продукт не найден.
        """

        for cell in self.cells.values():
            if product_id in cell.inventory:
                return cell

        return None

    @property
    def total_capacity(self) -> int:
        """Метод для получения общей емкости склада

        Returns:
            Количество товара, которое может уместиться в склад.
        """

        capacity = 0
        for cell in self.cells.values():
            capacity += cell.capacity

        return capacity

    @property
    def number_of_cells(self) -> int:
        """Метод получения количества ячеек на складе.

        Returns:
            Количество ячеек на складе.
        """

        return len(self.cells)
