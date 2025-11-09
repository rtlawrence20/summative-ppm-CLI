from utils import formatting


def test_print_users_plain_mode(capsys, monkeypatch, make_user):
    # Force plain mode
    monkeypatch.setattr(formatting, "HAS_RICH", False, raising=True)
    monkeypatch.setattr(formatting, "console", None, raising=True)
    formatting.print_users([make_user("Alex", None)])
    out = capsys.readouterr().out
    assert "Alex" in out
    assert " - " in out or " | - | " in out  # email shown as "-"


def test_print_projects_and_tasks_plain(capsys, monkeypatch, make_project, make_task):
    monkeypatch.setattr(formatting, "HAS_RICH", False, raising=True)
    monkeypatch.setattr(formatting, "console", None, raising=True)

    p = make_project(with_tasks=True)
    formatting.print_projects([p])
    t1 = p.tasks[0]
    formatting.print_tasks([(t1, p.id)], projects_by_id={p.id: p})
    out = capsys.readouterr().out
    assert p.title in out
    assert t1.title in out
