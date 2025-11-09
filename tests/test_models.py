import re


def test_user_creation_and_serialization(make_user):
    u = make_user(name="Bri", email=None)
    assert u.name == "Bri"
    # Email is optional now
    assert u.email is None
    d = u.to_dict()
    assert d["name"] == "Bri"
    assert "email" in d and d["email"] is None
    # Round-trip
    from models.user import User

    u2 = User.from_dict(d)
    assert u2.name == "Bri"
    assert u2.email is None
    assert u2.id == d["id"]


# Email validation applies if provided; optional otherwise
def test_user_invalid_email_raises_when_provided():
    from models.user import User
    import pytest

    with pytest.raises(ValueError):
        User(name="Nope", email="not-an-email")


def test_task_status_toggle(make_task):
    t = make_task("Do thing", status="todo")
    assert t.status == "todo"
    t.mark_complete()
    assert t.status == "done"
    t.mark_incomplete()
    assert t.status == "todo"


def test_project_add_task_and_serialize(make_project):
    p = make_project(with_tasks=True)
    assert len(p.tasks) == 2
    d = p.to_dict()
    assert "tasks" in d and len(d["tasks"]) == 2
    assert all(task["status"] in {"todo", "in_progress", "done"} for task in d["tasks"])
    # Round-trip
    from models.project import Project

    p2 = Project.from_dict(d)
    assert p2.title == p.title
    assert len(p2.tasks) == 2
