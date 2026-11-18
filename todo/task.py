"""Task model: one single to-do item.

Design choice: a dataclass keeps the Task small and readable. It only holds
data and knows how to turn itself into a dict (for saving) and back.
It does NOT know about files or the screen - this keeps each part simple.
"""
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    id: int
    title: str
    completed: bool = False
    # Stored as a text string so it is easy to save in JSON.
    created_at: str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M")
    )

    def to_dict(self) -> dict:
        """Convert the task to a plain dictionary (JSON friendly)."""
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Build a Task from a dictionary. Raises ValueError if data is bad."""
        try:
            return cls(
                id=int(data["id"]),
                title=str(data["title"]),
                completed=bool(data.get("completed", False)),
                created_at=str(data.get("created_at", "")),
            )
        except (KeyError, TypeError, ValueError) as err:
            raise ValueError(f"Invalid task data: {data!r}") from err
