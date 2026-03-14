from typing import Iterable
from src.models import Task
import requests
import logging

logger = logging.getLogger(__name__)


class ApiSource:
    """
    Источник задач, получающий их из внешнего API.

    :param url: URL-адрес API.
    """

    def __init__(self, url: str):
        self.url = url

    def get_tasks(self) -> Iterable[Task]:
        """
        Запрашивает данные из API и возвращает последовательность задач.

        :return: Итерируемый объект с задачами.
        :raises ValueError при ошибках получения данных из API.
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Вызовет исключение для статусов 4xx/5xx
            data = response.json()
            for item in data:
                try:
                    yield Task.create_task(item)
                except (ValueError, TypeError) as e:
                    logger.error(
                        f"Ошибка при создании задачи из данных API: {item}, ошибка: {e}"
                    )
                    continue
        except Exception as e:
            logger.error(f"Ошибка получения задач из JSON {self.url}: {e}")
            raise ValueError("Ошибка получения задач из JSON")

    @property
    def url(self) -> str:
        """Свойство для доступа к URL API."""
        return self._url

    @url.setter
    def url(self, url: str):
        """Сеттер для установки URL API."""
        self._url = url
