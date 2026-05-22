import enum
from dataclasses import dataclass
import datetime


class NodeStatus(enum.Enum):
    OPEN = "open"
    CLOSED = "closed"


@dataclass
class LogisticsNode:
    """Класс логистического узла."""

    id: int
    city: str
    address: str
    name: str
    opening_date: datetime.date
    closing_date: datetime.date | None
    status: NodeStatus
    manager_id: int | None


