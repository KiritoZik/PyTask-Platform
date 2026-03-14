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
│   └── test_models.py
│
└── README.md
```

## Архитектура

- **`src/models.py`**: Содержит модель данных `Task`.
- **`src/sources/`**: Директория с конкретными реализациями источников (`FileSource`, `GeneratorSource`, `ApiSource`).
- **`src/collector.py`**: Класс `TaskCollector`, который собирает задачи из разных источников.

## Тестирование

Для запуска тестов выполните команду в корневой директории проекта:

```bash
   python -m pytest --cov
```
