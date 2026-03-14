import pytest
from src.models import Task, TaskStatus


def test_task_creation():
    task = Task(task_id=101, info="Тестовая задача", priority=4, status=TaskStatus.NEW)
    assert task.task_id == 101
    assert task.info == "Тестовая задача"
    assert task.priority == 4
    assert task.status == TaskStatus.NEW
    assert task.created_date is not None


def test_is_ready_to_start_property():
    task_new = Task(task_id=1, info="a", priority=1, status=TaskStatus.NEW)
    task_done = Task(task_id=2, info="b", priority=2, status=TaskStatus.DONE)
    assert task_new.is_ready_to_start is True
    assert task_done.is_ready_to_start is False


def test_create_task_with_classmethod():
    task_data = {
        "task_id": 201,
        "info": "Задача из фабрики",
        "priority": 5,
        "status": "IN_PROGRESS",
    }
    task = Task.create_task(task_data)
    assert isinstance(task, Task)
    assert task.task_id == 201
    assert task.status == TaskStatus.IN_PROGRESS


def test_create_task_classmethod_missing_keys():
    task_data = {"task_id": 202, "info": "Неполная задача"}
    with pytest.raises(ValueError, match="Ошибка при инициализации задачи"):
        Task.create_task(task_data)
