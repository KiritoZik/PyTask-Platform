import pytest

from src.collector import TaskCollector
from src.models import Task, TaskStatus
from src.sources.generator_source import GeneratorSource
from src.task_queue import TaskQueue, TaskQueueIterator


def _make_task(task_id: int, priority: int, status: TaskStatus) -> Task:
    return Task(
        task_id=task_id,
        info=f"task-{task_id}",
        priority=priority,
        status=status,
    )


@pytest.fixture
def sample_tasks():
    return [
        _make_task(1, 1, TaskStatus.NEW),
        _make_task(2, 3, TaskStatus.IN_PROGRESS),
        _make_task(3, 5, TaskStatus.DONE),
        _make_task(4, 2, TaskStatus.NEW),
        _make_task(5, 4, TaskStatus.DONE),
    ]


def test_queue_works_with_for_list_sum(sample_tasks):
    queue = TaskQueue(sample_tasks)
    assert [t.task_id for t in queue] == [1, 2, 3, 4, 5]
    assert len(list(queue)) == 5
    assert sum(t.priority for t in queue) == 15


def test_queue_repeated_iteration_over_list(sample_tasks):
    queue = TaskQueue(sample_tasks)
    first = [t.task_id for t in queue]
    second = [t.task_id for t in queue]
    assert first == second == [1, 2, 3, 4, 5]


def test_queue_repeated_iteration_over_callable():
    def factory():
        yield _make_task(1, 1, TaskStatus.NEW)
        yield _make_task(2, 2, TaskStatus.DONE)

    queue = TaskQueue(factory)
    assert [t.task_id for t in queue] == [1, 2]
    assert [t.task_id for t in queue] == [1, 2]


def test_queue_iterator_protocol(sample_tasks):
    queue = TaskQueue(sample_tasks)
    iterator = iter(queue)
    assert isinstance(iterator, TaskQueueIterator)

    seen = [next(iterator).task_id for _ in sample_tasks]
    assert seen == [1, 2, 3, 4, 5]

    with pytest.raises(StopIteration):
        next(iterator)


def test_queue_iter_returns_fresh_iterator(sample_tasks):
    queue = TaskQueue(sample_tasks)
    it1 = iter(queue)
    it2 = iter(queue)
    assert it1 is not it2
    assert next(it1).task_id == 1
    assert next(it2).task_id == 1


def test_queue_filter_by_status_enum(sample_tasks):
    queue = TaskQueue(sample_tasks).filter_by_status(TaskStatus.NEW)
    assert [t.task_id for t in queue] == [1, 4]


def test_queue_filter_by_status_string(sample_tasks):
    queue = TaskQueue(sample_tasks).filter_by_status("done")
    assert [t.task_id for t in queue] == [3, 5]


def test_queue_filter_by_priority(sample_tasks):
    assert [t.task_id for t in TaskQueue(sample_tasks).filter_by_priority(3)] == [2]


def test_queue_generic_filter(sample_tasks):
    high = TaskQueue(sample_tasks).filter(lambda t: t.priority >= 3)
    assert [t.task_id for t in high] == [2, 3, 5]


def test_queue_filter_chaining(sample_tasks):
    queue = (
        TaskQueue(sample_tasks)
        .filter_by_status(TaskStatus.DONE)
        .filter(lambda t: t.priority >= 4)
    )
    assert [t.task_id for t in queue] == [3, 5]


def test_queue_filters_are_lazy():
    calls = {"n": 0}

    def factory():
        calls["n"] += 1
        yield _make_task(1, 1, TaskStatus.NEW)
        yield _make_task(2, 2, TaskStatus.DONE)

    filtered = TaskQueue(factory).filter_by_status(TaskStatus.NEW)
    assert calls["n"] == 0
    assert [t.task_id for t in filtered] == [1]
    assert calls["n"] == 1
    _ = list(filtered)
    assert calls["n"] == 2


def test_queue_handles_large_stream():
    def factory():
        for i in range(1, 100_001):
            yield _make_task(i, (i % 5) + 1, TaskStatus.NEW)

    queue = TaskQueue(factory).filter_by_priority(5)
    total = 0
    for task in queue:
        assert task.priority == 5
        total += 1
    assert total == 20_000


def test_queue_integration_with_collector():
    collector = TaskCollector(sources=[GeneratorSource(count=10)])
    queue = TaskQueue(collector.get_all_tasks)

    first_pass = [t.task_id for t in queue]
    second_pass = [t.task_id for t in queue]
    assert first_pass == second_pass
    assert len(first_pass) == 10

    priorities = sum(t.priority for t in queue.filter_by_status(TaskStatus.NEW))
    assert priorities > 0
