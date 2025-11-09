# utils/storage.py
from __future__ import annotations

import json
from pathlib import Path
from typing import List

# Model imports (match your existing files)
from models.user import User
from models.project import Project

# --- Paths ---
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

USERS_PATH = DATA_DIR / "users.json"
PROJECTS_PATH = DATA_DIR / "projects.json"


# --- Ensure files exist ---
def _ensure_file(path: Path) -> None:
    """
    Ensure the file exists. If not, create an empty JSON list file.
    """
    if not path.exists():
        path.write_text("[]", encoding="utf-8")


# --- Load/Save ---
def load_users() -> List[User]:
    """
    Load all users from disk. On malformed JSON, returns an empty list.
    """
    _ensure_file(USERS_PATH)
    try:
        raw = json.loads(USERS_PATH.read_text(encoding="utf-8"))
        return [User.from_dict(d) for d in raw]
    except json.JSONDecodeError:
        return []


def save_users(users: List[User]) -> None:
    """
    Save all users to disk.
    """
    serializable = [u.to_dict() for u in users]
    USERS_PATH.write_text(json.dumps(serializable, indent=2), encoding="utf-8")


def load_projects() -> List[Project]:
    """
    Load all projects from disk.
    On incorrect JSON, returns an empty list.
    """
    _ensure_file(PROJECTS_PATH)
    try:
        raw = json.loads(PROJECTS_PATH.read_text(encoding="utf-8"))
        return [Project.from_dict(d) for d in raw]
    except json.JSONDecodeError:
        return []


def save_projects(projects: List[Project]) -> None:
    """
    Save all projects to disk.
    """
    serializable = [p.to_dict() for p in projects]
    PROJECTS_PATH.write_text(json.dumps(serializable, indent=2), encoding="utf-8")


# --- Helpers lookup / indexing ---


def index_by_id(items):
    """
    Return a dict keyed by .id for any list of objects that have an id attribute.
    """
    return {getattr(i, "id"): i for i in items}


def get_user_by_name(users: List[User], name: str) -> User | None:
    """
    Case-insensitive user name lookup.
    """
    name_l = (name or "").strip().lower()
    for u in users:
        if u.name.strip().lower() == name_l:
            return u
    return None


def get_project_by_title(projects: List[Project], title: str) -> Project | None:
    """
    Case-insensitive project title lookup.
    """
    title_l = (title or "").strip().lower()
    for p in projects:
        if p.title.strip().lower() == title_l:
            return p
    return None
