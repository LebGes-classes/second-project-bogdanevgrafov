import datetime


DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def parse_date(value: str) -> datetime.date:
    """Метод преобразования строки в дату.

    Args:
        value: строка даты.

    Returns:
        Дата.
    """

    return datetime.datetime.strptime(value, DATE_FORMAT).date()


def format_date(value: datetime.date) -> str:
    """Метод преобразования даты в строку.

    Args:
        value: дата.

    Returns:
        Строка даты.
    """

    return value.strftime(DATE_FORMAT)


def parse_datetime(value: str) -> datetime.datetime:
    """Метод преобразования строки в дату и время.

    Args:
        value: строка даты и времени.

    Returns:
        Дата и время.
    """

    return datetime.datetime.strptime(value, DATETIME_FORMAT)


def format_datetime(value: datetime.datetime) -> str:
    """Метод преобразования даты и времени в строку.

    Args:
        value: дата и время.

    Returns:
        Строка даты и времени.
    """

    return value.strftime(DATETIME_FORMAT)

