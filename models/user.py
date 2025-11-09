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
        email (Optional[str]): Email address of the user (optional).
        created_at (str): ISO formatted creation timestamp.
    """

    def __init__(
        self, name: str, email: Optional[str] = None, user_id: Optional[str] = None
    ):
        self.name = name
        self.email = email  # will trigger setter below
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
    def email(self) -> Optional[str]:
        return self._email

    @email.setter  # <-- this line was missing
    def email(self, value: Optional[str]):
        if value is None or value == "":
            self._email = None
            return
        v = value.strip().lower()
        if not EMAIL_RE.match(v):
            raise ValueError("Invalid email address.")
        self._email = v

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,  # may be None; serialized as null
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        user = cls(data["name"], data.get("email"), data.get("id"))
        user.created_at = data.get("created_at", user.created_at)
        return user

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email or '-'})"

    def __str__(self) -> str:
        email = self.email or "-"
        return f"{self.name} <{email}>"
