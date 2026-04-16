import pytest
from datetime import date
from unittest.mock import patch, mock_open
from task import Task, TaskManager


@pytest.fixture
def manager(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return TaskManager()


def test_add_task(manager):
    task = manager.add("テストタスク")
    assert task.id == 1
    assert task.title == "テストタスク"
    assert task.done is False


def test_add_task_with_due_date(manager):
    due = date(2026, 5, 1)
    task = manager.add("期限付きタスク", due_date=due)
    assert task.due_date == due


def test_complete_task(manager):
    task = manager.add("完了テスト")
    result = manager.complete(task.id)
    assert result is True
    assert manager.tasks[0].done is True


def test_complete_nonexistent_task(manager):
    result = manager.complete(999)
    assert result is False


def test_delete_task(manager):
    task = manager.add("削除テスト")
    result = manager.delete(task.id)
    assert result is True
    assert len(manager.tasks) == 0


def test_list_tasks_excludes_done(manager):
    manager.add("未完了")
    task2 = manager.add("完了済み")
    manager.complete(task2.id)
    tasks = manager.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "未完了"


def test_list_tasks_sorted_by_due_date(manager):
    manager.add("後", due_date=date(2026, 5, 10))
    manager.add("先", due_date=date(2026, 5, 1))
    tasks = manager.list_tasks()
    assert tasks[0].title == "先"


def test_priority_stored_correctly(manager):
    task = manager.add("高優先度", priority="high")
    assert task.priority == "high"
