"""TaskManager: the 'brain' of the app (business logic).

Design choice: all rules (add, remove, complete) live here, with NO input()
or print() calls. That makes it easy to test and to reuse with a different
interface (for example a web page) later.
"""
from typing import List, Optional

from .task import Task
from .storage import JsonStorage

MAX_TITLE_LENGTH = 100


class TaskError(Exception):
    """Base class for errors caused by bad task operations."""


class InvalidTaskError(TaskError):
    """The title is empty or too long."""


class TaskNotFoundError(TaskError):
    """No task with the given id exists."""


class TaskManager:
    def __init__(self, storage: JsonStorage):
        self.storage = storage
        self.tasks: List[Task] = []
        self._next_id_value = 1
        self._load()

    # ---------- internal helpers ----------
    def _load(self) -> None:
        """Load tasks from storage, skipping any entry that is broken."""
        data = self.storage.load()
        for item in data["tasks"]:
            try:
                self.tasks.append(Task.from_dict(item))
            except ValueError:
                continue  # Skip bad entries instead of crashing.
        # Counter must be bigger than every id already in use.
        saved = data.get("next_id", 1)
        highest = max((t.id for t in self.tasks), default=0)
        self._next_id_value = max(int(saved) if str(saved).isdigit() else 1,
                                  highest + 1)

    def _save(self) -> None:
        self.storage.save({"next_id": self._next_id_value,
                           "tasks": [t.to_dict() for t in self.tasks]})

    def _next_id(self) -> int:
        # A saved counter that only goes up, so an id is NEVER reused,
        # even after the newest task is deleted (max+1 would reuse it).
        new_id = self._next_id_value
        self._next_id_value += 1
        return new_id

    def _find(self, task_id: int) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(f"No task with id {task_id}.")

    # ---------- public features ----------
    def add_task(self, title: str) -> Task:
        title = (title or "").strip()
        if not title:
            raise InvalidTaskError("Task title cannot be empty.")
        if len(title) > MAX_TITLE_LENGTH:
            raise InvalidTaskError(
                f"Task title is too long (max {MAX_TITLE_LENGTH} characters)."
            )
        task = Task(id=self._next_id(), title=title)
        self.tasks.append(task)
        self._save()
        return task

    def remove_task(self, task_id: int) -> Task:
        task = self._find(task_id)
        self.tasks.remove(task)
        self._save()
        return task

    def complete_task(self, task_id: int) -> Task:
        task = self._find(task_id)
        if task.completed:
            raise TaskError(f"Task {task_id} is already completed.")
        task.completed = True
        self._save()
        return task

    def list_tasks(self, completed: Optional[bool] = None) -> List[Task]:
        """completed=None -> all, True -> done only, False -> pending only."""
        if completed is None:
            return list(self.tasks)
        return [t for t in self.tasks if t.completed == completed]
