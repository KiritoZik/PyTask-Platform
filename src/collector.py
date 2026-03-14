import logging
from typing import Iterable, Sequence
from src.decorators.contracts import TaskSource
from src.models import Task

logger = logging.getLogger(__name__)


class TaskCollector:
    """
    Собирает задачи из различных источников.

    :param sources: Последовательность источников задач, соответствующих контракту TaskSource.
    """

    def __init__(self, sources: Sequence[TaskSource] = ()):
        self.sources = sources

    def get_all_tasks(self) -> Iterable[Task]:
        """
        Собирает и возвращает все задачи из всех предоставленных источников.

        :return: Итерируемый объект со всеми собранными задачами.
        """
        for src in self.sources:
            if not isinstance(src, TaskSource):
                logger.warning(
                    f"Источник {type(src).__name__} пропущен, так как не соответствует контракту TaskSource."
                )
                continue
            try:
                yield from src.get_tasks()
            except Exception as e:
                logger.error(
                    f"Ошибка при получении задач из источника {type(src).__name__}: {e}"
                )
                continue
