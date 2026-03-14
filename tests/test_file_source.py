import pytest
from src.sources.file_source import FileSource
from src.models import TaskStatus


def test_file_source_success(tmp_path):
    tasks_content = (
        "info=Купить молоко;task_id=1;priority=3;status=NEW\n"
        "info=Выполнить задание;task_id=2;priority=5;status=DONE"
    )
    tasks_file = tmp_path / "tasks.txt"
    tasks_file.write_text(tasks_content, encoding="utf-8")

    source = FileSource(path=tasks_file)
    tasks = list(source.get_tasks())

    assert len(tasks) == 2
    assert tasks[0].info == "Купить молоко"
    assert tasks[1].status == TaskStatus.DONE


def test_file_source_file_not_found():
    source = FileSource(path="non_existent_file.txt")
    with pytest.raises(ValueError, match="Ошибка чтения файла"):
        list(source.get_tasks())


def test_file_source_empty_file(tmp_path):
    tasks_file = tmp_path / "tasks.txt"
    tasks_file.write_text("", encoding="utf-8")
    source = FileSource(path=tasks_file)
    tasks = list(source.get_tasks())
    assert len(tasks) == 0


def test_file_source_invalid_lines(tmp_path):
    tasks_content = "просто текст без разделителей\nkey_without_value=\n;;\n"
    tasks_file = tmp_path / "tasks.txt"
    tasks_file.write_text(tasks_content, encoding="utf-8")
    source = FileSource(path=tasks_file)
    tasks = list(source.get_tasks())
    assert len(tasks) == 0


def test_parse_payload_static_method():
    payload_str = "task_id=10;priority=4;status=IN_PROGRESS"
    payload = FileSource.parse_payload(payload_str)
    assert payload["task_id"] == 10
    assert payload["priority"] == 4
    assert payload["status"] == "IN_PROGRESS"
