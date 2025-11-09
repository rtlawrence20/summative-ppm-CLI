import uuid
from datetime import datetime, timezone
from typing import Optional

VALID_STATUSES = {"todo", "in_progress", "done"}


class Task:
    """
    Represents a task within a project.
    Attributes:
        id (str): Unique identifier for the task.
        title (str): Title of the task.
        status (str): Status of the task; one of "todo", "in_progress", "done".
        assigned_to (Optional[str]): User ID of the assignee, or None.
        created_at (str): ISO formatted creation timestamp.
    """

    def __init__(
        self,
        title: str,
        task_id: Optional[str] = None,
        status: str = "todo",
        assigned_to: Optional[str] = None,
        created_at: Optional[str] = None,
    ):
        self.title = title
        self.id = task_id if task_id else str(uuid.uuid4())
        self.status = status  # setter validates
        self.assigned_to = assigned_to  # user.id or None
        self.created_at = created_at or datetime.now(tz=timezone.utc).isoformat()

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Task title must be a non-empty string.")
        self._title = value.strip()

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        v = (value or "").strip().lower()
        if v not in VALID_STATUSES:
            raise ValueError(f"Status must be one of {sorted(VALID_STATUSES)}.")
        self._status = v

    @property
    def completed(self) -> bool:
        return self.status == "done"

    def mark_complete(self):
        self.status = "done"

    def mark_incomplete(self):
        self.status = "todo"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "assigned_to": self.assigned_to,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            title=data["title"],
            task_id=data["id"],
            status=data.get("status", "todo"),
            assigned_to=data.get("assigned_to"),
            created_at=data.get("created_at"),
        )

    def __repr__(self):
        badge = "✓" if self.completed else "○"
        return f"Task({badge} {self.title}, status={self.status}, assigned_to={self.assigned_to or '-'})"
