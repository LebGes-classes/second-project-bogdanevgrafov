from dataclasses import dataclass
from CRM_project.models.product import Product

@dataclass
class WarehouseCell():
    """Класс ячейки склада."""
    id: int
    name: str
    capacity: int
    inventory: dict[int, int] # id товара: количество

    def add(self, product: Product, quantity: int = 1) -> None:
        """Метод для добавления товара в ячейку склада.

        Args:
            product: товар, который нужно добавить.
            quantity: количество товара, которое нужно добавить.
        """
        if self.capacity < sum(self.inventory.values()) + quantity:
            raise ValueError("Недостаточно места в ячейке склада.")

        if product.id in self.inventory:
            self.inventory[product.id] += quantity
        else:
            self.inventory[product.id] = quantity

    def remove(self, product: Product, quantity: int = 1) -> None:
        """Метод для удаления товара из ячейки склада.

        Args:
            product: товар, который нужно удалить.
            quantity: количество товара, которое нужно удалить.
        """
        if product.id not in self.inventory:
            raise ValueError("Товар не найден в ячейке склада.")

        if self.inventory[product.id] < quantity:
            raise ValueError("Недостаточно товара в ячейке склада.")

        self.inventory[product.id] -= quantity

        if self.inventory[product.id] == 0:
            del self.inventory[product.id]

    def has(self, product: Product, quantity: int = 1) -> bool:
        """Метод для проверки наличия товара в ячейке склада.

        Args:
            product: товар, который нужно проверить.
            quantity: количество товара, которое нужно проверить.

        Returns:
            True, если товар есть в ячейке склада в нужном количестве, иначе False.
        """

        return self.inventory.get(product.id, 0) >= quantity

    @property
    def available_capacity(self) -> int:
        """Метод для получения доступной емкости ячейки склада.

        Returns:
            Доступная емкость ячейки склада.
        """

        return self.capacity - sum(self.inventory.values())

    def get_quantity(self, product: Product) -> int:
        """Метод для получения количества товара в ячейке склада.

        Args:
            product: товар, количество которого нужно получить.

        Returns:
            Количество товара в ячейке склада.
        """

        return self.inventory.get(product.id, 0)

    def to_dict(self) -> dict:
        """Метод для вывода информации о ячейке склада в виде словаря.

        Returns:
            Словарь с информацией о ячейке склада.
        """
        return {
            "id": self.id,
            "name": self.name,
            "capacity": self.capacity,
            "inventory": self.inventory,
        }

