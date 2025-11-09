# utils/formatting.py
from __future__ import annotations

from typing import Iterable, Optional, Any

# Try to use Rich; otherwise fall back to plain printing
try:
    from rich.console import Console
    from rich.table import Table

    HAS_RICH = True
    console: Optional[Console] = Console()
except Exception:  # pragma: no cover
    HAS_RICH = False
    console = None  # type: ignore


# --- Table printing functions ---
def _materialize(it: Iterable[Any]) -> list[list[str]]:
    """
    Convert iterable of rows into a list of stringified rows.
    Each row may be a tuple/list.
    """
    out: list[list[str]] = []
    for row in it:
        if isinstance(row, (list, tuple)):
            out.append([str(x) for x in row])
        else:
            out.append([str(row)])
    return out


def _plain_table(headers: list[str], rows: Iterable[Iterable[Any]]) -> None:
    """
    Fallback printer when 'rich' isn't installed.
    This function first materializes 'rows' so widths can be computed safely.
    """
    rows_list = _materialize(rows)

    widths = [len(h) for h in headers]
    for r in rows_list:
        for i, cell in enumerate(r):
            if i < len(widths):
                widths[i] = max(widths[i], len(cell))
            else:
                # more cells than headers; extend widths
                widths.append(len(cell))

    # header
    header_line = " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    sep = "-+-".join("-" * widths[i] for i in range(len(widths)))
    print(header_line)
    print(sep)

    # rows
    for r in rows_list:
        # pad short rows
        padded = r + [""] * (len(widths) - len(r))
        print(" | ".join(padded[i].ljust(widths[i]) for i in range(len(widths))))


def print_users(users) -> None:
    """
    Pretty-print a list of User objects (id, name, created_at).
    """
    headers = ["ID", "Name", "Created At"]
    rows = (
        (getattr(u, "id", "-"), getattr(u, "name", "-"), getattr(u, "created_at", "-"))
        for u in users
    )

    if HAS_RICH and console is not None:
        table = Table(title="Users")
        for h in headers:
            table.add_column(h)
        for row in rows:
            table.add_row(*[str(x) for x in row])
        console.print(table)
    else:
        _plain_table(headers, rows)


def print_projects(projects, users_by_id: Optional[dict] = None) -> None:
    """
    Pretty-print projects with owner and task count.
    """
    headers = ["ID", "Title", "Owner", "Tasks", "Created At"]

    def owner_name(user_id: Optional[str]) -> str:
        if users_by_id and user_id in users_by_id:
            return getattr(users_by_id[user_id], "name", "-")
        return "-"

    rows = (
        (
            getattr(p, "id", "-"),
            getattr(p, "title", "-"),
            owner_name(getattr(p, "user_id", None)),
            len(getattr(p, "tasks", []) or []),
            getattr(p, "created_at", "-"),
        )
        for p in projects
    )

    if HAS_RICH and console is not None:
        table = Table(title="Projects")
        for h in headers:
            table.add_column(h)
        for row in rows:
            table.add_row(*[str(x) for x in row])
        console.print(table)
    else:
        _plain_table(headers, rows)


def print_tasks(tasks, projects_by_id: Optional[dict] = None) -> None:
    """
    Pretty-print tasks.
    If projects_by_id is provided, will show project titles.
    """
    headers = ["ID", "Title", "Project", "Completed", "Created At"]

    def project_title(pid: Optional[str]) -> str:
        if pid and projects_by_id and pid in projects_by_id:
            return getattr(projects_by_id[pid], "title", "-")
        return "-"

    norm_rows = []

    for item in tasks:
        # (Task, project_id) tuple
        if isinstance(item, tuple) and len(item) == 2:
            task, pid = item
            tid = getattr(task, "id", "-")
            ttitle = getattr(task, "title", "-")
            tcreated = getattr(task, "created_at", "-")
            tcompleted = bool(getattr(task, "completed", False))
            norm_rows.append((tid, ttitle, project_title(pid), tcompleted, tcreated))
            continue

        # Dict-like
        if isinstance(item, dict):
            tid = item.get("id", "-")
            ttitle = item.get("title", "-")
            tcreated = item.get("created_at", "-")
            tcompleted = bool(item.get("completed", False))
            # Try to derive project title if a project_id was included
            pid = item.get("project_id")
            norm_rows.append((tid, ttitle, project_title(pid), tcompleted, tcreated))
            continue

        # Assume Task object
        tid = getattr(item, "id", "-")
        ttitle = getattr(item, "title", "-")
        tcreated = getattr(item, "created_at", "-")
        tcompleted = bool(getattr(item, "completed", False))
        norm_rows.append((tid, ttitle, "-", tcompleted, tcreated))

    if HAS_RICH and console is not None:
        table = Table(title="Tasks")
        for h in headers:
            table.add_column(h)
        for row in norm_rows:
            table.add_row(*[str(x) for x in row])
        console.print(table)
    else:
        _plain_table(headers, norm_rows)


def print_all_tasks_from_projects(projects) -> None:
    """
    Convenience:
    flatten tasks from a list of projects and print them with project titles.
    """
    projects_by_id = {
        getattr(p, "id", None): p for p in projects if getattr(p, "id", None)
    }
    flattened = []
    for p in projects:
        pid = getattr(p, "id", None)
        for t in getattr(p, "tasks", []) or []:
            flattened.append((t, pid))
    print_tasks(flattened, projects_by_id=projects_by_id)
