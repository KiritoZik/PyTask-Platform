from pathlib import Path
from typing import Iterable, Dict, Union
import logging
from src.models import Task

logger = logging.getLogger(__name__)


class FileSource:
    """
    Источник задач, загружающий их из текстового файла.
    """

    def __init__(self, path: Union[str, Path]):
        self.path = Path(path)

    def get_tasks(self) -> Iterable[Task]:
        """
        Читает файл и возвращает последовательность задач.
        """
        try:
            with self.path.open("r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue

                    payload = self.parse_payload(line)

                    try:
                        if payload:
                            if "task_id" in payload:
                                payload["task_id"] = int(payload["task_id"])
                            if "priority" in payload:
                                payload["priority"] = int(payload["priority"])
                            yield Task.create_task(payload)
                    except (ValueError, TypeError) as e:
                        logger.error(f"Строка {line_num}: Ошибка создания задачи - {e}")
                        continue
        except FileNotFoundError:
            logger.error(f"Ошибка чтения файла: {self.path}")
            raise ValueError("Ошибка чтения файла")

    @staticmethod
    def parse_payload(payload_str: str) -> Dict:
        """
        Парсит строку 'key1=val1;key2=val2' в словарь.
        """
        payload = {}
        for part in payload_str.split(";"):
            if "=" in part:
                key, value = part.split("=", 1)
                payload[key.strip()] = value.strip()
        return payload
