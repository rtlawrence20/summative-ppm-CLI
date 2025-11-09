from __future__ import annotations

import json
import sys
from pathlib import Path
import types
import pytest


# --- Ensure project root is importable (so `from utils import storage` works) ---
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture(autouse=True)
def isolate_storage_paths(tmp_path, monkeypatch):
    """
    Redirect utils.storage's DATA_DIR/USERS_PATH/PROJECTS_PATH to a temp dir.
    Initializes empty JSON arrays so tests start from a clean slate.
    """
    from utils import storage

    data_dir = tmp_path / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    users_path = data_dir / "users.json"
    projects_path = data_dir / "projects.json"

    users_path.write_text("[]", encoding="utf-8")
    projects_path.write_text("[]", encoding="utf-8")

    # Point storage module at our temp files
    monkeypatch.setattr(storage, "DATA_DIR", data_dir, raising=True)
    monkeypatch.setattr(storage, "USERS_PATH", users_path, raising=True)
    monkeypatch.setattr(storage, "PROJECTS_PATH", projects_path, raising=True)

    # Useful if a test wants to inspect the files afterward
    return types.SimpleNamespace(
        DATA_DIR=data_dir, USERS_PATH=users_path, PROJECTS_PATH=projects_path
    )


@pytest.fixture
def make_user():
    from models.user import User

    def _make(name="Alex", email="alex@example.com"):
        return User(name=name, email=email)

    return _make


@pytest.fixture
def make_task():
    """
    Your Task model uses `status` (todo/in_progress/done), not `completed`.
    """
    from models.task import Task

    def _make(title="Sample Task", status="todo"):
        return Task(title=title, status=status)

    return _make


@pytest.fixture
def make_project(make_task):
    from models.project import Project

    def _make(title="CLI Tool", user_id="user-1", with_tasks=False):
        p = Project(title=title, user_id=user_id)
        if with_tasks:
            p.add_task(make_task("Implement add-task", status="todo"))
            p.add_task(make_task("Write tests", status="in_progress"))
        return p

    return _make
