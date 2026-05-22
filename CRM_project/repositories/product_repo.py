from CRM_project.models.product import Product
from CRM_project.repositories.base_repository import BaseRepository


class ProductRepository(BaseRepository):
    """Класс репозитория товаров."""

    def list(self) -> list[Product]:
        """Метод получения списка товаров.

        Returns:
            Список товаров.
        """

        return [self._from_dict(item) for item in self._read()]

    def get(self, product_id: int) -> Product | None:
        """Метод получения товара по ID.

        Args:
            product_id: идентификатор товара.

        Returns:
            Товар или None.
        """

        for item in self.list():
            if item.id == product_id:
                return item
        return None

    def add(self, product: Product) -> None:
        """Метод добавления товара.

        Args:
            product: товар.
        """

        items = self.list()
        if any(existing.id == product.id for existing in items):
            raise ValueError("Товар с таким ID уже существует.")
        items.append(product)
        self._write([self._to_dict(item) for item in items])

    def update(self, product: Product) -> None:
        """Метод обновления товара.

        Args:
            product: товар.
        """

        items = self.list()
        updated = False
        for index, item in enumerate(items):
            if item.id == product.id:
                items[index] = product
                updated = True
                break
        if not updated:
            raise ValueError("Товар не найден.")
        self._write([self._to_dict(item) for item in items])

    def _from_dict(self, data: dict) -> Product:
        return Product(
            id=int(data["id"]),
            name=data["name"],
            price=float(data["price"]),
            weight=float(data["weight"]),
            developer=data["developer"],
            is_available=bool(data.get("is_available", True)),
        )

    def _to_dict(self, product: Product) -> dict:
        return {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "weight": product.weight,
            "developer": product.developer,
            "is_available": product.is_available,
        }

