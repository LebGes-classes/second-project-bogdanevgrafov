from CRM_project.models.warehouse import Warehouse
from CRM_project.models.warehouse_cell import WarehouseCell
from CRM_project.repositories.base_repository import BaseRepository
from CRM_project.utils.serialization import format_date, parse_date
from CRM_project.models.logistics_node import NodeStatus


class WarehouseRepository(BaseRepository):
    """Класс репозитория складов."""

    def list(self) -> list[Warehouse]:
        """Метод получения списка складов.

        Returns:
            Список складов.
        """

        return [self._from_dict(item) for item in self._read()]

    def get(self, warehouse_id: int) -> Warehouse | None:
        """Метод получения склада по ID.

        Args:
            warehouse_id: идентификатор склада.

        Returns:
            Склад или None.
        """

        for item in self.list():
            if item.id == warehouse_id:
                return item
        return None

    def add(self, warehouse: Warehouse) -> None:
        """Метод добавления склада.

        Args:
            warehouse: склад.
        """

        items = self.list()
        if any(existing.id == warehouse.id for existing in items):
            raise ValueError("Склад с таким ID уже существует.")
        items.append(warehouse)
        self._write([self._to_dict(item) for item in items])

    def update(self, warehouse: Warehouse) -> None:
        """Метод обновления склада.

        Args:
            warehouse: склад.
        """

        items = self.list()
        updated = False
        for index, item in enumerate(items):
            if item.id == warehouse.id:
                items[index] = warehouse
                updated = True
                break
        if not updated:
            raise ValueError("Склад не найден.")
        self._write([self._to_dict(item) for item in items])

    def _from_dict(self, data: dict) -> Warehouse:
        cells: dict[int, WarehouseCell] = {}
        for cell_data in data.get("cells", []):
            cell = WarehouseCell(
                id=int(cell_data["id"]),
                name=cell_data["name"],
                capacity=int(cell_data["capacity"]),
                inventory={int(k): int(v) for k, v in cell_data.get("inventory", {}).items()},
            )
            cells[cell.id] = cell
        return Warehouse(
            id=int(data["id"]),
            city=data["city"],
            address=data["address"],
            name=data["name"],
            opening_date=parse_date(data["opening_date"]),
            closing_date=parse_date(data["closing_date"]) if data.get("closing_date") else None,
            status=NodeStatus(data["status"]),
            cells=cells,
            manager_id=data.get("manager_id"),
        )

    def _to_dict(self, warehouse: Warehouse) -> dict:
        return {
            "id": warehouse.id,
            "city": warehouse.city,
            "address": warehouse.address,
            "name": warehouse.name,
            "opening_date": format_date(warehouse.opening_date),
            "closing_date": format_date(warehouse.closing_date) if warehouse.closing_date else None,
            "status": warehouse.status.value,
            "manager_id": warehouse.manager_id,
            "cells": [cell.to_dict() for cell in warehouse.cells.values()],
        }

