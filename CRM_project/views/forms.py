import datetime

from CRM_project.utils.serialization import DATE_FORMAT


def input_int(prompt: str) -> int:
    """Метод ввода целого числа.

    Args:
        prompt: подсказка.

    Returns:
        Число.
    """

    while True:
        raw = input(prompt)
        try:
            return int(raw)
        except ValueError:
            print("Введите целое число.")


def input_float(prompt: str) -> float:
    """Метод ввода числа с плавающей точкой.

    Args:
        prompt: подсказка.

    Returns:
        Число.
    """

    while True:
        raw = input(prompt)
        try:
            return float(raw)
        except ValueError:
            print("Введите число.")


def input_str(prompt: str) -> str:
    """Метод ввода строки.

    Args:
        prompt: подсказка.

    Returns:
        Строка.
    """

    while True:
        raw = input(prompt).strip()
        if raw:
            return raw
        print("Поле не может быть пустым.")


def input_date(prompt: str) -> datetime.date:
    """Метод ввода даты.

    Args:
        prompt: подсказка.

    Returns:
        Дата.
    """

    while True:
        raw = input(f"{prompt} ({DATE_FORMAT}): ")
        try:
            return datetime.datetime.strptime(raw, DATE_FORMAT).date()
        except ValueError:
            print("Неверный формат даты.")

