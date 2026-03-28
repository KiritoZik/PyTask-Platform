class TaskValidationError(ValueError):
    """Некорректные данные задачи (наследует ValueError для источников)."""


class InvalidTaskIdError(TaskValidationError):
    """Недопустимый task_id."""


class InvalidDescriptionError(TaskValidationError):
    """Недопустимое описание."""


class InvalidPriorityError(TaskValidationError):
    """Недопустимый приоритет."""


class InvalidStatusError(TaskValidationError):
    """Недопустимый статус."""
