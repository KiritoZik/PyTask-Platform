from datetime import datetime
from typing import Literal
from enum import Enum


class TaskStatus(Enum):
    """Перечисление возможных статусов задачи."""

    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class Task:
    """
    Класс для представления задачи.

    :param task_id: Уникальный идентификатор задачи.
    :param info: Описание задачи.
    :param priority: Приоритет задачи (от 1 до 5).
    :param status: Текущий статус задачи.
    """

    def __init__(
        self,
        task_id: int,
        info: str,
        priority: Literal[1, 2, 3, 4, 5],
        status: TaskStatus,
    ):
        self.task_id = task_id
        self.info = info
        self.priority = priority
        self.status = status
        self.created_date = datetime.now()

    @property
    def is_ready_to_start(self) -> bool:
        """
        Проверяет, готова ли задача к выполнению.
        :return: True, если статус задачи 'NEW', иначе False.
        """
        return self.status == TaskStatus.NEW

    @classmethod
    def create_task(cls, data: dict):
        """
        Фабричный метод для создания задачи из словаря.
        :param data: Словарь с данными для создания задачи.
        :return: Экземпляр класса Task.
        :raises ValueError: Если в словаре отсутствуют обязательные ключи.
        """
        required = ["task_id", "info", "priority"]
        if not all(key in data for key in required):
            raise ValueError(
                "Ошибка при инициализации задачи: отсутствуют обязательные поля."
            )
        data["status"] = TaskStatus(data["status"].upper())

        return cls(**data)
