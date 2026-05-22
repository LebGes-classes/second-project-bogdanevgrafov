from CRM_project.models.customer import Customer
from CRM_project.models.product import Product
from CRM_project.repositories.customer_repo import CustomerRepository
from CRM_project.repositories.product_repo import ProductRepository


class RegistryController:
    """Класс контроллера справочников."""

    def __init__(self, product_repo: ProductRepository, customer_repo: CustomerRepository) -> None:
        """Метод инициализации контроллера.

        Args:
            product_repo: репозиторий товаров.
            customer_repo: репозиторий покупателей.
        """

        self.product_repo = product_repo
        self.customer_repo = customer_repo

    def add_product(self, product: Product) -> None:
        """Метод добавления товара.

        Args:
            product: товар.
        """

        self.product_repo.add(product)

    def add_customer(self, customer: Customer) -> None:
        """Метод добавления покупателя.

        Args:
            customer: покупатель.
        """

        self.customer_repo.add(customer)

