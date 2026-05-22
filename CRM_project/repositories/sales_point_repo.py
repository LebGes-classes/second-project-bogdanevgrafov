from CRM_project.models.sales_point import SalesPoint
from CRM_project.repositories.base_repository import BaseRepository
from CRM_project.utils.serialization import format_date, parse_date
from CRM_project.models.logistics_node import NodeStatus


class SalesPointRepository(BaseRepository):
    """Класс репозитория пунктов продаж."""

    def list(self) -> list[SalesPoint]:
        """Метод получения списка пунктов продаж.

        Returns:
            Список пунктов продаж.
        """

        return [self._from_dict(item) for item in self._read()]

    def get(self, sales_point_id: int) -> SalesPoint | None:
        """Метод получения пункта продаж по ID.

        Args:
            sales_point_id: идентификатор пункта продаж.

        Returns:
            Пункт продаж или None.
        """

        for item in self.list():
            if item.id == sales_point_id:
                return item
        return None

    def add(self, sales_point: SalesPoint) -> None:
        """Метод добавления пункта продаж.

        Args:
            sales_point: пункт продаж.
        """

        items = self.list()
        if any(existing.id == sales_point.id for existing in items):
            raise ValueError("Пункт продаж с таким ID уже существует.")
        items.append(sales_point)
        self._write([self._to_dict(item) for item in items])

    def update(self, sales_point: SalesPoint) -> None:
        """Метод обновления пункта продаж.

        Args:
            sales_point: пункт продаж.
        """

        items = self.list()
        updated = False
        for index, item in enumerate(items):
            if item.id == sales_point.id:
                items[index] = sales_point
                updated = True
                break
        if not updated:
            raise ValueError("Пункт продаж не найден.")
        self._write([self._to_dict(item) for item in items])

    def _from_dict(self, data: dict) -> SalesPoint:
        return SalesPoint(
            id=int(data["id"]),
            city=data["city"],
            address=data["address"],
            name=data["name"],
            opening_date=parse_date(data["opening_date"]),
            closing_date=parse_date(data["closing_date"]) if data.get("closing_date") else None,
            status=NodeStatus(data["status"]),
            inventory={int(k): int(v) for k, v in data.get("inventory", {}).items()},
            manager_id=data.get("manager_id"),
        )

    def _to_dict(self, sales_point: SalesPoint) -> dict:
        return {
            "id": sales_point.id,
            "city": sales_point.city,
            "address": sales_point.address,
            "name": sales_point.name,
            "opening_date": format_date(sales_point.opening_date),
            "closing_date": format_date(sales_point.closing_date) if sales_point.closing_date else None,
            "status": sales_point.status.value,
            "manager_id": sales_point.manager_id,
            "inventory": {str(k): v for k, v in sales_point.inventory.items()},
        }

