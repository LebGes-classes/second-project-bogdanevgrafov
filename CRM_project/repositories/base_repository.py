import json
import os


class BaseRepository:
    """Класс базового репозитория."""

    def __init__(self, file_path: str) -> None:
        """Метод инициализации репозитория.

        Args:
            file_path: путь к файлу.
        """

        self.file_path = file_path

    def _read(self) -> list[dict]:
        """Метод чтения данных из файла.

        Returns:
            Список словарей.
        """

        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _write(self, data: list[dict]) -> None:
        """Метод записи данных в файл.

        Args:
            data: список словарей.
        """

        dir_name = os.path.dirname(self.file_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

