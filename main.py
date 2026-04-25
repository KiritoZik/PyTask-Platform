from logging import config

from src.collector import TaskCollector
from src.common.config import LOGGING_CONFIG
from src.models import TaskStatus
from src.sources.generator_source import GeneratorSource
from src.task_queue import TaskQueue

config.dictConfig(LOGGING_CONFIG)


if __name__ == "__main__":
    collector = TaskCollector(sources=[GeneratorSource(count=20)])
    queue = TaskQueue(collector.get_all_tasks)

    print("Все задачи в очереди:")
    for task in queue:
        print(f"  #{task.task_id} priority={task.priority} status={task.status.value}")

    print("\nNEW с приоритетом >= 4:")
    urgent = queue.filter_by_status(TaskStatus.NEW).filter(lambda t: t.priority >= 4)
    for task in urgent:
        print(f"  #{task.task_id} priority={task.priority}")
