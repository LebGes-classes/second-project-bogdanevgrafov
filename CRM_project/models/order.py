import datetime
import enum
from dataclasses import dataclass


class OrderStatus(enum.Enum):
    """Статусы заказа."""

    SOLD = "sold"
    RETURNED = "returned"


@dataclass
class Order:
    """Класс заказа."""

    id: int
    customer_id: int
    items: dict[int, int]
    total_amount: float
    status: OrderStatus
    created_at: datetime.datetime
    sales_point_id: int

