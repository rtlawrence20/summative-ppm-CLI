import re
import uuid
from datetime import datetime, timezone
from typing import Optional

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class User:
    """
    Represents a user in the system.
    Attributes:
        id (str): Unique identifier for the user.
        name (str): Name of the user.
        email (str): Email address of the user.
        created_at (str): ISO formatted creation timestamp.
    """

    def __init__(self, name: str, email: str, user_id: Optional[str] = None):
        self.name = name
        self.email = email  # property setter
        self.id = user_id if user_id else str(uuid.uuid4())
        self.created_at = datetime.now(tz=timezone.utc).isoformat()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("User name must be a non-empty string.")
        self._name = value.strip()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        v = (value or "").strip().lower()
        if not EMAIL_RE.match(v):
            raise ValueError("Invalid email address.")
        self._email = v

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        user = cls(data["name"], data["email"], data["id"])
        user.created_at = data.get("created_at", user.created_at)
        return user

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email})"
