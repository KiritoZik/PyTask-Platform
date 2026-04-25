from typing import Callable, Iterable, Iterator, Union

from src.models import Task, TaskStatus

Source = Union[Iterable[Task], Callable[[], Iterable[Task]]]


class TaskQueueIterator:
    """
    Итератор очереди задач.
    """

    __slots__ = ("_it",)

    def __init__(self, iterable: Iterable[Task]) -> None:
        self._it = iter(iterable)

    def __iter__(self) -> "TaskQueueIterator":
        return self

    def __next__(self) -> Task:
        return next(self._it)


class TaskQueue:
    """
    Ленивая коллекция задач с повторным обходом и фильтрацией.
    Фильтры возвращают новый ``TaskQueue`` и не хранит задачи в памяти.
    """

    __slots__ = ("_factory",)

    def __init__(self, source: Source) -> None:
        if callable(source):
            self._factory: Callable[[], Iterable[Task]] = source
        elif hasattr(source, "__next__"):
            raise TypeError(
                "TaskQueue не принимает одноразовые итераторы"
            )
        elif hasattr(source, "__iter__"):
            self._factory = lambda: source
        else:
            raise TypeError("source должен быть итерируемым или callable.")

    def __iter__(self) -> TaskQueueIterator:
        return TaskQueueIterator(self._factory())

    def filter(self, predicate: Callable[[Task], bool]) -> "TaskQueue":
        """Ленивый фильтр по произвольному предикату."""
        def gen() -> Iterator[Task]:
            for task in self:
                if predicate(task):
                    yield task

        return TaskQueue(gen)

    def filter_by_status(self, status: Union[TaskStatus, str]) -> "TaskQueue":
        """Ленивый фильтр по статусу."""
        if isinstance(status, str):
            status = TaskStatus[status.upper()]
        return self.filter(lambda t: t.status == status)

    def filter_by_priority(self, priority: int) -> "TaskQueue":
        """Ленивый фильтр по равенству приоритета (1..5)."""
        return self.filter(lambda t: t.priority == priority)
