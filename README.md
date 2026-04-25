# Платформа для сбора задач

Выполнил:
Ямалов Искандер, М8О-106БВ-25

## Описание

Система собирает задачи, которые могут поступать из разных источников:
- **FileSource**: Загрузка из текстового файла.
- **GeneratorSource**: Программная генерация .
- **ApiSource**: Получение из внешнего  API.


## Структура проекта

```
PyTask-Platform/
├── src/
│   ├── __init__.py
│   ├── collector.py
│   ├── models.py
│   ├── task_queue.py
│   └── sources/
│       ├── __init__.py
│       ├── api_source.py
│       ├── file_source.py
│       └── generator_source.py
│
├── tests/
│   ├── __init__.py
│   ├── test_api_source.py
│   ├── test_collector.py
│   ├── test_file_source.py
│   ├── test_generator_source.py
│   ├── test_models.py
│   └── test_task_queue.py
│
└── README.md
```

## Архитектура

- **`src/models.py`**: Содержит модель данных `Task`.
- **`src/sources/`**: Директория с конкретными реализациями источников (`FileSource`, `GeneratorSource`, `ApiSource`).
- **`src/collector.py`**: Класс `TaskCollector`, который собирает задачи из разных источников.
- **`src/task_queue.py`**: Класс `TaskQueue` и `TaskQueueIterator` — ленивая очередь задач с итерацией и фильтрацией.

## TaskQueue

`TaskQueue` — итерируемая коллекция-обёртка над произвольным источником
задач. Источником может быть:

- повторно проходимая коллекция (`list`, `tuple`, ...);
- callable без аргументов, возвращающий итератор (например,
  `TaskCollector.get_all_tasks` или генератор-функция).

Одноразовые итераторы недопускаются, чтобы не потерять случайно данные.

### Возможности

- Протокол итерации: `__iter__` возвращает новый `TaskQueueIterator` , поэтому очередь можно проходить сколько угодно раз.
- Ленивые фильтры, возвращающие новый `TaskQueue`:
  - `filter(predicate)` — фильтр по произвольному предикату;
  - `filter_by_status(status)` — по `TaskStatus` или имени статуса;
  - `filter_by_priority(priority)` — по равенству приоритета.
- Фильтры можно сцеплять друг к другу; вычисления запускаются только при реальном
  обходе, задачи не хранятся в памяти.
- Совместимость со стандартными конструкциями Python: `for`, `list(...)`,
  `sum(...)`, генераторные выражения.

### Пример использования

```python
from src.collector import TaskCollector
from src.models import TaskStatus
from src.sources.generator_source import GeneratorSource
from src.task_queue import TaskQueue

collector = TaskCollector(sources=[GeneratorSource(count=100)])
queue = TaskQueue(collector.get_all_tasks)

urgent_new = queue.filter_by_status(TaskStatus.NEW).filter(lambda t: t.priority >= 4)

for task in urgent_new:
    print(task.task_id, task.priority)

total_priority = sum(t.priority for t in queue)
```

## Тестирование

Для запуска тестов выполните команду в корневой директории проекта:

```bash
   python -m pytest --cov
```
