from src.sources.generator_source import GeneratorSource
from src.models import Task


def test_generator_source_generates_correct_count():
    source = GeneratorSource(count=5)
    tasks = list(source.get_tasks())
    assert len(tasks) == 5


def test_generator_source_task_properties():
    source = GeneratorSource(count=10)
    tasks = list(source.get_tasks())
    last_task = tasks[-1]

    assert isinstance(last_task, Task)
    assert last_task.task_id == 9010
    assert last_task.priority == 1  # 10 % 5 + 1 = 1
    assert "Сгенерированная задача №10" in last_task.info


def test_generator_source_with_zero_count():
    source = GeneratorSource(count=0)
    tasks = list(source.get_tasks())
    assert len(tasks) == 0


def test_generator_source_with_one_count():
    source = GeneratorSource(count=1)
    tasks = list(source.get_tasks())
    assert len(tasks) == 1
    task = tasks[0]
    assert task.task_id == 9001
    assert "Сгенерированная задача №1" in task.info
