from src.collector import TaskCollector
from src.sources.file_source import FileSource
from src.sources.generator_source import GeneratorSource


def test_collector_with_valid_sources(tmp_path):
    tasks_content = "info=Файловая задача;task_id=1;priority=1;status=NEW"
    tasks_file = tmp_path / "tasks.txt"
    tasks_file.write_text(tasks_content, encoding="utf-8")
    file_source = FileSource(path=tasks_file)

    generator_source = GeneratorSource(count=3)

    collector = TaskCollector(sources=[file_source, generator_source])
    tasks = list(collector.get_all_tasks())

    assert len(tasks) == 4


def test_collector_with_no_sources():
    collector = TaskCollector(sources=[])
    tasks = list(collector.get_all_tasks())
    assert len(tasks) == 0


def test_collector_ignores_invalid_source():
    class BrokenSource:
        pass

    valid_source = GeneratorSource(count=2)
    collector = TaskCollector(sources=[BrokenSource(), valid_source])
    tasks = list(collector.get_all_tasks())

    assert len(tasks) == 2
