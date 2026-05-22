import datetime

from CRM_project.models.order import Order, OrderStatus
from CRM_project.repositories.customer_repo import CustomerRepository
from CRM_project.repositories.order_repo import OrderRepository
from CRM_project.repositories.product_repo import ProductRepository
from CRM_project.repositories.sales_point_repo import SalesPointRepository


class SalesController:
    """Класс контроллера продаж."""

    def __init__(
        self,
        product_repo: ProductRepository,
        sales_point_repo: SalesPointRepository,
        order_repo: OrderRepository,
        customer_repo: CustomerRepository,
    ) -> None:
        """Метод инициализации контроллера.

        Args:
            product_repo: репозиторий товаров.
            sales_point_repo: репозиторий пунктов продаж.
            order_repo: репозиторий заказов.
            customer_repo: репозиторий покупателей.
        """

        self.product_repo = product_repo
        self.sales_point_repo = sales_point_repo
        self.order_repo = order_repo
        self.customer_repo = customer_repo

    def sell_product(self, sales_point_id: int, product_id: int, quantity: int, customer_id: int) -> None:
        """Метод продажи товара.

        Args:
            sales_point_id: идентификатор пункта продаж.
            product_id: идентификатор товара.
            quantity: количество.
            customer_id: идентификатор покупателя.
        """

        sales_point = self._require_sales_point(sales_point_id)
        product = self._require_product(product_id)
        customer = self._require_customer(customer_id)
        if not sales_point.has(product, quantity):
            raise ValueError("Недостаточно товара в пункте продаж.")
        sales_point.remove(product, quantity)
        order = Order(
            id=self._next_order_id(),
            customer_id=customer.id,
            items={product.id: quantity},
            total_amount=product.price * quantity,
            status=OrderStatus.SOLD,
            created_at=datetime.datetime.now(),
            sales_point_id=sales_point.id,
        )
        customer.order_list.append(order.id)
        self.sales_point_repo.update(sales_point)
        self.order_repo.add(order)
        self.customer_repo.update(customer)

    def return_order(self, order_id: int) -> None:
        """Метод возврата заказа.

        Args:
            order_id: идентификатор заказа.
        """

        order = self._require_order(order_id)
        if order.status == OrderStatus.RETURNED:
            raise ValueError("Заказ уже возвращен.")
        sales_point = self._require_sales_point(order.sales_point_id)
        for product_id, quantity in order.items.items():
            product = self._require_product(product_id)
            sales_point.add(product, quantity)
        order.status = OrderStatus.RETURNED
        self.sales_point_repo.update(sales_point)
        self.order_repo.update(order)

    def _next_order_id(self) -> int:
        orders = self.order_repo.list()
        return max((order.id for order in orders), default=0) + 1

    def _require_sales_point(self, sales_point_id: int):
        sales_point = self.sales_point_repo.get(sales_point_id)
        if sales_point is None:
            raise ValueError("Пункт продаж не найден.")
        return sales_point

    def _require_product(self, product_id: int):
        product = self.product_repo.get(product_id)
        if product is None:
            raise ValueError("Товар не найден.")
        return product

    def _require_customer(self, customer_id: int):
        customer = self.customer_repo.get(customer_id)
        if customer is None:
            raise ValueError("Покупатель не найден.")
        return customer

    def _require_order(self, order_id: int):
        order = self.order_repo.get(order_id)
        if order is None:
            raise ValueError("Заказ не найден.")
        return order

