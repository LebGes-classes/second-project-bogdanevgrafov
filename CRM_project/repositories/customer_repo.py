from CRM_project.models.customer import Customer
from CRM_project.models.base_person import Gender
from CRM_project.repositories.base_repository import BaseRepository
from CRM_project.utils.serialization import format_date, parse_date


class CustomerRepository(BaseRepository):
    """Класс репозитория покупателей."""

    def list(self) -> list[Customer]:
        """Метод получения списка покупателей.

        Returns:
            Список покупателей.
        """

        return [self._from_dict(item) for item in self._read()]

    def get(self, customer_id: int) -> Customer | None:
        """Метод получения покупателя по ID.

        Args:
            customer_id: идентификатор покупателя.

        Returns:
            Покупатель или None.
        """

        for item in self.list():
            if item.id == customer_id:
                return item
        return None

    def add(self, customer: Customer) -> None:
        """Метод добавления покупателя.

        Args:
            customer: покупатель.
        """

        items = self.list()
        if any(existing.id == customer.id for existing in items):
            raise ValueError("Покупатель с таким ID уже существует.")
        items.append(customer)
        self._write([self._to_dict(item) for item in items])

    def update(self, customer: Customer) -> None:
        """Метод обновления покупателя.

        Args:
            customer: покупатель.
        """

        items = self.list()
        updated = False
        for index, item in enumerate(items):
            if item.id == customer.id:
                items[index] = customer
                updated = True
                break
        if not updated:
            raise ValueError("Покупатель не найден.")
        self._write([self._to_dict(item) for item in items])

    def _from_dict(self, data: dict) -> Customer:
        return Customer(
            id=int(data["id"]),
            first_name=data["first_name"],
            second_name=data["second_name"],
            date_of_birth=parse_date(data["date_of_birth"]),
            sex=Gender(data["sex"]),
            phone_number=data["phone_number"],
            email=data["email"],
            password=data["password"],
            country=data["country"],
            city=data["city"],
            address=data["address"],
            order_list=data.get("order_list", []),
        )

    def _to_dict(self, customer: Customer) -> dict:
        return {
            "id": customer.id,
            "first_name": customer.first_name,
            "second_name": customer.second_name,
            "date_of_birth": format_date(customer.date_of_birth),
            "sex": customer.sex.value,
            "phone_number": customer.phone_number,
            "email": customer.email,
            "password": customer.password,
            "country": customer.country,
            "city": customer.city,
            "address": customer.address,
            "order_list": customer.order_list,
        }

