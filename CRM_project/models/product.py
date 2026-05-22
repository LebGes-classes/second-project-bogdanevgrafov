from dataclasses import dataclass

@dataclass
class Product:
    """Класс товара.

    Args:
         id: Уникальный идентификатор
         name: Название
         price: Стоимость
         weight: Масса
         developer: Страна производитель
         is_available: Доступен ли к закупке
    """

    id: int
    name: str
    price: float
    weight: float
    developer: str
    is_available: bool = True


