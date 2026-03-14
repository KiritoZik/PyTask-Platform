import pytest
from unittest.mock import patch, MagicMock
from src.sources.api_source import ApiSource
from src.models import Task, TaskStatus


@patch("requests.get")
def test_api_source_get_tasks_success(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"task_id": 1, "info": "API Task 1", "priority": 1, "status": "NEW"},
        {"task_id": 2, "info": "API Task 2", "priority": 2, "status": "IN_PROGRESS"},
    ]
    mock_get.return_value = mock_response

    source = ApiSource(url="http://fake-api.com/tasks")
    tasks = list(source.get_tasks())

    assert len(tasks) == 2
    assert all(isinstance(t, Task) for t in tasks)
    assert tasks[0].task_id == 1
    assert tasks[1].status == TaskStatus.IN_PROGRESS


@patch("requests.get")
def test_api_source_get_tasks_http_error(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("HTTP Error")
    mock_get.return_value = mock_response

    source = ApiSource(url="http://fake-api.com/tasks")

    with pytest.raises(ValueError, match="Ошибка получения задач из JSON"):
        list(source.get_tasks())
