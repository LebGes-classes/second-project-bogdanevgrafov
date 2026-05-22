from CRM_project.models.order import Order, OrderStatus
from CRM_project.repositories.base_repository import BaseRepository
from CRM_project.utils.serialization import format_datetime, parse_datetime


class OrderRepository(BaseRepository):
    """Класс репозитория заказов."""

    def list(self) -> list[Order]:
        """Метод получения списка заказов.

        Returns:
            Список заказов.
        """

        return [self._from_dict(item) for item in self._read()]

    def get(self, order_id: int) -> Order | None:
        """Метод получения заказа по ID.

        Args:
            order_id: идентификатор заказа.

        Returns:
            Заказ или None.
        """

        for item in self.list():
            if item.id == order_id:
                return item
        return None

    def add(self, order: Order) -> None:
        """Метод добавления заказа.

        Args:
            order: заказ.
        """

        items = self.list()
        if any(existing.id == order.id for existing in items):
            raise ValueError("Заказ с таким ID уже существует.")
        items.append(order)
        self._write([self._to_dict(item) for item in items])

    def update(self, order: Order) -> None:
        """Метод обновления заказа.

        Args:
            order: заказ.
        """

        items = self.list()
        updated = False
        for index, item in enumerate(items):
            if item.id == order.id:
                items[index] = order
                updated = True
                break
        if not updated:
            raise ValueError("Заказ не найден.")
        self._write([self._to_dict(item) for item in items])

    def _from_dict(self, data: dict) -> Order:
        return Order(
            id=int(data["id"]),
            customer_id=int(data["customer_id"]),
            items={int(k): int(v) for k, v in data.get("items", {}).items()},
            total_amount=float(data["total_amount"]),
            status=OrderStatus(data["status"]),
            created_at=parse_datetime(data["created_at"]),
            sales_point_id=int(data["sales_point_id"]),
        )

    def _to_dict(self, order: Order) -> dict:
        return {
            "id": order.id,
            "customer_id": order.customer_id,
            "items": {str(k): v for k, v in order.items.items()},
            "total_amount": order.total_amount,
            "status": order.status.value,
            "created_at": format_datetime(order.created_at),
            "sales_point_id": order.sales_point_id,
        }

