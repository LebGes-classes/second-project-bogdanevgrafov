import datetime

from CRM_project.models.logistics_node import NodeStatus
from CRM_project.models.sales_point import SalesPoint
from CRM_project.models.warehouse import Warehouse
from CRM_project.repositories.sales_point_repo import SalesPointRepository
from CRM_project.repositories.warehouse_repo import WarehouseRepository


class LogisticsController:
    """Класс контроллера логистики."""

    def __init__(
        self,
        warehouse_repo: WarehouseRepository,
        sales_point_repo: SalesPointRepository,
    ) -> None:
        """Метод инициализации контроллера.

        Args:
            warehouse_repo: репозиторий складов.
            sales_point_repo: репозиторий пунктов продаж.
        """

        self.warehouse_repo = warehouse_repo
        self.sales_point_repo = sales_point_repo

    def open_warehouse(self, node_id: int, city: str, address: str, name: str) -> None:
        """Метод открытия склада.

        Args:
            node_id: идентификатор склада.
            city: город.
            address: адрес.
            name: название.
        """

        warehouse = Warehouse(
            id=node_id,
            city=city,
            address=address,
            name=name,
            opening_date=datetime.date.today(),
            closing_date=None,
            status=NodeStatus.OPEN,
            cells={},
            manager_id=None,
        )
        self.warehouse_repo.add(warehouse)

    def close_warehouse(self, node_id: int) -> None:
        """Метод закрытия склада.

        Args:
            node_id: идентификатор склада.
        """

        warehouse = self._require_warehouse(node_id)
        warehouse.status = NodeStatus.CLOSED
        warehouse.closing_date = datetime.date.today()
        self.warehouse_repo.update(warehouse)

    def open_sales_point(self, node_id: int, city: str, address: str, name: str) -> None:
        """Метод открытия пункта продаж.

        Args:
            node_id: идентификатор пункта.
            city: город.
            address: адрес.
            name: название.
        """

        sales_point = SalesPoint(
            id=node_id,
            city=city,
            address=address,
            name=name,
            opening_date=datetime.date.today(),
            closing_date=None,
            status=NodeStatus.OPEN,
            inventory={},
            manager_id=None,
        )
        self.sales_point_repo.add(sales_point)

    def close_sales_point(self, node_id: int) -> None:
        """Метод закрытия пункта продаж.

        Args:
            node_id: идентификатор пункта.
        """

        sales_point = self._require_sales_point(node_id)
        sales_point.status = NodeStatus.CLOSED
        sales_point.closing_date = datetime.date.today()
        self.sales_point_repo.update(sales_point)

    def _require_warehouse(self, warehouse_id: int) -> Warehouse:
        warehouse = self.warehouse_repo.get(warehouse_id)
        if warehouse is None:
            raise ValueError("Склад не найден.")
        return warehouse

    def _require_sales_point(self, sales_point_id: int) -> SalesPoint:
        sales_point = self.sales_point_repo.get(sales_point_id)
        if sales_point is None:
            raise ValueError("Пункт продаж не найден.")
        return sales_point

