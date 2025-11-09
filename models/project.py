from datetime import datetime, timezone
from typing import List, Optional
import uuid
from models.task import Task


class Project:
    """
    Represents a project in the system.
    Attributes:
        id (str): Unique identifier for the project.
        title (str): Title of the project.
        user_id (str): ID of the user who owns the project.
        description (str): Description of the project.
        due_date (Optional[str]): Due date of the project, if any.
        tasks (List[Task]): List of tasks associated with the project.
        created_at (str): ISO formatted creation timestamp.
    """

    def __init__(
        self,
        title: str,
        user_id: str,
        project_id: Optional[str] = None,
        description: str = "",
        due_date: Optional[str] = None,
    ):
        self.title = title
        self.id = project_id if project_id else str(uuid.uuid4())
        self.user_id = user_id
        self.description = description or ""
        self._due_date = None
        if due_date:
            self.due_date = due_date  # property setter parses/normalizes
        self.tasks: List[Task] = []
        self.created_at = datetime.now(tz=timezone.utc).isoformat()

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Project title must be a non-empty string.")
        self._title = value.strip()

    @property
    def due_date(self) -> Optional[str]:
        return self._due_date

    @due_date.setter
    def due_date(self, value: str):
        # accept flexible inputs; normalize to YYYY-MM-DD
        try:
            # no external dep version:
            dt = (
                datetime.fromisoformat(value)
                if "T" in value
                else datetime.strptime(value, "%Y-%m-%d")
            )
            self._due_date = dt.date().isoformat()
        except Exception:
            raise ValueError("due_date must be ISO (YYYY-MM-DD) or ISO datetime")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "user_id": self.user_id,
            "description": self.description,
            "due_date": self.due_date,
            "tasks": [t.to_dict() for t in self.tasks],
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        project = cls(
            data["title"],
            data["user_id"],
            data.get("id"),
            description=data.get("description", ""),
            due_date=data.get("due_date"),
        )
        project.created_at = data.get("created_at", project.created_at)
        project.tasks = [Task.from_dict(td) for td in data.get("tasks", [])]
        return project

    def __repr__(self):
        return f"Project(id={self.id}, title={self.title}, due={self.due_date or '-'}, tasks={len(self.tasks)})"
