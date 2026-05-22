from typing import Sequence


def choose(title: str, options: Sequence[str], allow_zero: bool = True) -> int:
    """Метод показа меню и выбора пункта.

    Args:
        title: заголовок.
        options: список пунктов.
        allow_zero: разрешить пункт назад.

    Returns:
        Номер пункта.
    """

    print("\n" + title)
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")
    if allow_zero:
        print("0. Назад")
    while True:
        raw = input("Выберите пункт: ")
        try:
            value = int(raw)
        except ValueError:
            print("Введите число.")
            continue
        if allow_zero and value == 0:
            return 0
        if 1 <= value <= len(options):
            return value
        print("Неверный пункт меню.")


def show_message(text: str) -> None:
    """Метод вывода сообщения.

    Args:
        text: текст.
    """

    print(text)


def show_error(text: str) -> None:
    """Метод вывода ошибки.

    Args:
        text: текст.
    """

    print(f"Ошибка: {text}")

