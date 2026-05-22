from CRM_project.models.product import Product


def print_kv(title: str, data: dict) -> None:
    """Метод печати словаря.

    Args:
        title: заголовок.
        data: данные.
    """

    print("\n" + title)
    for key, value in data.items():
        print(f"{key}: {value}")


def print_inventory(title: str, inventory: dict[int, int], products: dict[int, Product]) -> None:
    """Метод печати товаров.

    Args:
        title: заголовок.
        inventory: товары и количество.
        products: словарь товаров.
    """

    print("\n" + title)
    if not inventory:
        print("Нет товаров.")
        return
    for product_id, quantity in inventory.items():
        product = products.get(product_id)
        name = product.name if product else "Неизвестный товар"
        print(f"{product_id} | {name} | {quantity}")

