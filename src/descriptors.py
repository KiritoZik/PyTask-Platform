from enum import Enum
from typing import Any
from src.task_exceptions import (
    InvalidDescriptionError,
    InvalidPriorityError,
    InvalidStatusError,
    InvalidTaskIdError,
)


class DataDescr:
    """Общий ``__get__``: значение лежит в слоте, имя в ``storage``."""

    __slots__ = ("storage",)

    def __init__(self, storage: str) -> None:
        self.storage = storage

    def __get__(self, instance: object | None, _) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.storage)


class ValidatedPositiveId(DataDescr):
    """task_id: целое > 0."""

    def __set__(self, instance: object, value: object) -> None:
        if not isinstance(value, int) or isinstance(value, bool):
            raise InvalidTaskIdError("task_id — целое число (не bool).")
        if value <= 0:
            raise InvalidTaskIdError("task_id должен быть > 0.")
        setattr(instance, self.storage, value)


class ValidatedDescription(DataDescr):
    """Непустая строка."""

    def __set__(self, instance: object, value: object) -> None:
        if not isinstance(value, str):
            raise InvalidDescriptionError("описание — строка.")
        s = value.strip()
        if not s:
            raise InvalidDescriptionError("описание не может быть пустым.")
        setattr(instance, self.storage, s)


class ValidatedPriority(DataDescr):
    """Целое от 1 до 5."""

    def __set__(self, instance: object, value: object) -> None:
        if not isinstance(value, int) or isinstance(value, bool):
            raise InvalidPriorityError("приоритет — целое число (не bool).")
        if value < 1 or value > 5:
            raise InvalidPriorityError("приоритет от 1 до 5.")
        setattr(instance, self.storage, value)


class ValidatedEnum(DataDescr):
    """TaskStatus или строка (имя или значение enum)."""

    def __init__(self, storage: str, enum_cls: type[Enum]) -> None:
        super().__init__(storage)
        self._enum = enum_cls

    def __set__(self, instance: object, value: object) -> None:
        if isinstance(value, self._enum):
            setattr(instance, self.storage, value)
            return
        if not isinstance(value, str):
            raise InvalidStatusError("недопустимый статус задачи.")
        key = value.upper()
        if key in self._enum.__members__:
            setattr(instance, self.storage, self._enum[key])
            return
        try:
            setattr(instance, self.storage, self._enum(value))
        except ValueError:
            raise InvalidStatusError("недопустимый статус задачи.")


class ReadOnlyCreatedAt(DataDescr):
    """Non-data: ``__set__`` нет — только наследуемый ``__get__`` (дата задаётся в ``Task.__init__``)."""
