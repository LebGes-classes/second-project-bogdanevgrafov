from dataclasses import dataclass

from CRM_project.models.logistics_node import LogisticsNode
from CRM_project.models.product import Product


@dataclass
class SalesPoint(LogisticsNode):
    """Класс пункта продаж."""

    inventory: dict[int, int]

    def add(self, product: Product, quantity: int = 1) -> None:
        """Метод добавления товара в пункт продаж.

        Args:
            product: товар для добавления.
            quantity: количество.
        """

        if product.id in self.inventory:
            self.inventory[product.id] += quantity
        else:
            self.inventory[product.id] = quantity

    def remove(self, product: Product, quantity: int = 1) -> None:
        """Метод удаления товара из пункта продаж.

        Args:
            product: товар для удаления.
            quantity: количество.
        """

        if product.id not in self.inventory:
            raise ValueError("Товар не найден в пункте продаж.")
        if self.inventory[product.id] < quantity:
            raise ValueError("Недостаточно товара в пункте продаж.")
        self.inventory[product.id] -= quantity
        if self.inventory[product.id] == 0:
            del self.inventory[product.id]

    def has(self, product: Product, quantity: int = 1) -> bool:
        """Метод проверки наличия товара в пункте продаж.

        Args:
            product: товар для проверки.
            quantity: количество.

        Returns:
            True, если товара достаточно.
        """

        return self.inventory.get(product.id, 0) >= quantity
