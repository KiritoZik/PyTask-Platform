from typing import Iterable
from src.models import Task
import logging

logger = logging.getLogger(__name__)


class GeneratorSource:
    """
    Источник, который генерирует задачи программно.

    :param count: Количество задач для генерации.
    """

    def __init__(self, count: int):
        self.count = count

    def get_tasks(self) -> Iterable[Task]:
        """
        Генерирует и возвращает последовательность задач.

        :return: Итерируемый объект с задачами.
        """
        for i in range(1, self.count + 1):
            payload = {
                "task_id": 9000 + i,
                "info": f"Сгенерированная задача №{i}",
                "priority": i % 5 + 1,
                "status": "NEW",
            }

            try:
                yield Task.create_task(payload)
            except Exception as e:
                logger.error(f"Ошибка при создании задачи: {e}")
                continue

    @property
    def count(self) -> int:
        """Свойство для доступа к количеству генерируемых задач."""
        return self._count

    @count.setter
    def count(self, count: int):
        """Сеттер для установки количества генерируемых задач."""
        self._count = count
