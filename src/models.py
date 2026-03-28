from datetime import datetime
from enum import Enum
from typing import Literal, cast

from src.descriptors import (
    ReadOnlyCreatedAt,
    ValidatedDescription,
    ValidatedEnum,
    ValidatedPositiveId,
    ValidatedPriority,
)
from src.task_exceptions import TaskValidationError


class TaskStatus(Enum):
    """Перечисление возможных статусов задачи."""

    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class Task:
    """
    Задача платформы обработки: инкапсулированное состояние и валидация через дескрипторы.

    :param task_id: id > 0
    :param info: непустая строка
    :param priority: 1..5
    :param status: TaskStatus
    """

    __slots__ = (
        "_task_id",
        "_info",
        "_priority",
        "_status",
        "_created_at",
    )

    task_id = ValidatedPositiveId("_task_id")
    info = ValidatedDescription("_info")
    priority = ValidatedPriority("_priority")
    status = ValidatedEnum("_status", TaskStatus)
    created_date = ReadOnlyCreatedAt("_created_at")

    def __init__(
        self,
        task_id: int,
        info: str,
        priority: Literal[1, 2, 3, 4, 5],
        status: TaskStatus,
    ) -> None:
        object.__setattr__(self, "_created_at", datetime.now())
        self.task_id = task_id
        self.info = info
        self.priority = priority
        self.status = status

    @property
    def is_ready_to_start(self) -> bool:
        """
        Проверяет, готова ли задача к выполнению.
        :return: True, если статус задачи 'NEW', иначе False.
        """
        return self.status == TaskStatus.NEW

    @classmethod
    def create_task(cls, data: dict) -> "Task":
        """
        Фабричный метод: создаёт ``Task`` из словаря.

        Нужны ключи task_id, info, priority, status. Исходный ``data`` не меняется.
        """
        d = dict(data)
        need = ("task_id", "info", "priority", "status")
        if not all(k in d for k in need):
            raise TaskValidationError("Нужны ключи: task_id, info, priority, status.")
        try:
            tid, pr = int(d["task_id"]), int(d["priority"])
        except (TypeError, ValueError):
            raise TaskValidationError("task_id и priority должны быть числами.")
        return cls(
            task_id=tid,
            info=str(d["info"]),
            priority=cast(Literal[1, 2, 3, 4, 5], pr),
            status=d["status"],
        )
