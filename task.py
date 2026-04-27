from dataclasses import dataclass
from datetime import date
from typing import Optional
import json
import os

STORAGE_FILE = "tasks.json"


@dataclass
class Task:
    id: int
    title: str
    done: bool = False
    due_date: Optional[date] = None
    priority: str = "medium"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "priority": self.priority,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        due = data.get("due_date")
        return cls(
            id=data["id"],
            title=data["title"],
            done=data.get("done", False),
            due_date=date.fromisoformat(due) if due else None,
            priority=data.get("priority", "medium"),
        )


class TaskManager:
    def __init__(self):
        self.tasks: list[Task] = []
        self._next_id = 1
        self._load()

    def add(self, title: str, due_date: Optional[date] = None, priority: str = "medium") -> Task:
        task = Task(id=self._next_id, title=title, due_date=due_date, priority=priority)
        self._next_id += 1
        self.tasks.append(task)
        self._save()
        return task

    def complete(self, task_id: int) -> bool:
        task = self._find(task_id)
        if task is None:
            return False
        task.done = True
        self._save()
        return True

    def delete(self, task_id: int) -> bool:
        task = self._find(task_id)
        if task is None:
            return False
        self.tasks.remove(task)
        self._save()
        return True

    def list_tasks(self, show_done: bool = False, priority: Optional[str] = None) -> list[Task]:
        tasks = self.tasks if show_done else [t for t in self.tasks if not t.done]
        if priority:
            tasks = [t for t in tasks if t.priority == priority]
        return sorted(tasks, key=lambda t: (t.due_date or date.max, t.priority))

    def _find(self, task_id: int) -> Optional[Task]:
        return next((t for t in self.tasks if t.id == task_id), None)

    def _save(self):
        with open(STORAGE_FILE, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=2)

    def _load(self):
        if not os.path.exists(STORAGE_FILE):
            return
        with open(STORAGE_FILE) as f:
            data = json.load(f)
        self.tasks = [Task.from_dict(d) for d in data]
        self._next_id = max((t.id for t in self.tasks), default=0) + 1
