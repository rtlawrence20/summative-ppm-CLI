from __future__ import annotations

import argparse
from typing import Optional, List, Tuple

from models.user import User
from models.project import Project
from models.task import Task

from utils.storage import (
    load_users,
    save_users,
    load_projects,
    save_projects,
    get_user_by_name,
    get_project_by_title,
    index_by_id,
)

from utils.formatting import (
    print_users,
    print_projects,
    print_tasks,
    console,
)

# ------------- Helpers ------------- #


def _info(msg: str) -> None:
    """
    Print a green info line if rich console is available; else plain print.
    """
    if console:
        console.print(f"[green]{msg}[/green]")
    else:
        print(msg)


def _warn(msg: str) -> None:
    """
    Print a yellow warning line if rich console is available; else plain print.
    """
    if console:
        console.print(f"[yellow]{msg}[/yellow]")
    else:
        print(msg)


def _error(msg: str) -> None:
    """
    Print a red error line if rich console is available; else plain print.
    """
    if console:
        console.print(f"[red]{msg}[/red]")
    else:
        print(msg)


def _flatten_tasks_with_project_id(projects: List[Project]) -> List[Tuple[Task, str]]:
    """
    Return a flat list of (task, project_id) pairs to feed print_tasks().
    """
    flat: List[Tuple[Task, str]] = []
    for p in projects:
        for t in getattr(p, "tasks", []) or []:
            flat.append((t, p.id))
    return flat


def _find_task_by_id(
    projects: List[Project], task_id: str
) -> tuple[Optional[Task], Optional[Project]]:
    """
    Locate a task by UUID across all projects. Returns (task, parent_project) or (None, None).
    """
    for p in projects:
        for t in getattr(p, "tasks", []) or []:
            if getattr(t, "id", None) == task_id:
                return t, p
    return None, None


# ------------- Command Handlers ------------- #


def cmd_add_user(args: argparse.Namespace) -> None:
    """
    Add a new user.
    """
    users = load_users()
    name = args.name.strip()
    email = (args.email or "").strip().lower()

    # Guard against duplicates by name; if email provided, also check duplicates by email
    for u in users:
        if u.name.lower() == name.lower():
            _warn(f"User with name '{name}' already exists.")
            return
        if email and (getattr(u, "email", "") or "").lower() == email:
            _warn(f"User with email '{email}' already exists.")
            return

    user = User(name=name, email=(email or None))
    users.append(user)
    save_users(users)
    _info(f"User created: {user}")
    print_users(users)


def cmd_list_users(_args: argparse.Namespace) -> None:
    """List all users."""
    users = load_users()
    if not users:
        _warn("No users found.")
        return
    print_users(users)


def cmd_add_project(args: argparse.Namespace) -> None:
    """
    Create a project for a user.
    """
    users = load_users()
    projects = load_projects()

    owner = get_user_by_name(users, args.user)
    if not owner:
        _error(f"No such user: {args.user}")
        return

    title = args.title.strip()
    # Optional: warn if project title exists for this owner
    for p in projects:
        if p.title.strip().lower() == title.lower() and p.user_id == owner.id:
            _warn(f"Project '{title}' already exists for user '{owner.name}'.")
            break

    proj = Project(title=title, user_id=owner.id)
    projects.append(proj)
    save_projects(projects)
    _info(f"Project created: {proj}")
    print_projects(projects, users_by_id=index_by_id(users))


def cmd_list_projects(args: argparse.Namespace) -> None:
    """
    List projects, optionally filtered by user.
    """
    users = load_users()
    projects = load_projects()

    if args.user:
        owner = get_user_by_name(users, args.user)
        if not owner:
            _error(f"No such user: {args.user}")
            return
        projects = [p for p in projects if p.user_id == owner.id]

    if not projects:
        _warn("No projects found.")
        return

    print_projects(projects, users_by_id=index_by_id(users))


def cmd_add_task(args: argparse.Namespace) -> None:
    """
    Add a task to a project.
    """
    projects = load_projects()
    proj = get_project_by_title(projects, args.project)
    if not proj:
        _error(f"No such project: {args.project}")
        return

    title = args.title.strip()
    task = Task(title=title)
    proj.add_task(task)
    save_projects(projects)
    _info(f"Task created: {task} in project '{proj.title}'")

    # Show tasks for this project only
    print_tasks([(t, proj.id) for t in proj.tasks], projects_by_id={proj.id: proj})


def cmd_list_tasks(args: argparse.Namespace) -> None:
    """
    List tasks, optionally filtered by project.
    """
    projects = load_projects()

    if args.project:
        proj = get_project_by_title(projects, args.project)
        if not proj:
            _error(f"No such project: {args.project}")
            return
        if not proj.tasks:
            _warn(f"No tasks found for project '{proj.title}'.")
            return
        print_tasks([(t, proj.id) for t in proj.tasks], projects_by_id={proj.id: proj})
        return

    # All tasks across all projects
    flat = _flatten_tasks_with_project_id(projects)
    if not flat:
        _warn("No tasks found.")
        return
    projects_by_id = {p.id: p for p in projects}
    print_tasks(flat, projects_by_id=projects_by_id)


def cmd_complete_task(args: argparse.Namespace) -> None:
    """
    Mark a task as completed by its UUID.
    """
    projects = load_projects()
    tid = args.id.strip()
    task, parent = _find_task_by_id(projects, tid)
    if not task or not parent:
        _error(f"No such task id: {tid}")
        return
    if getattr(task, "completed", False):
        _warn(f"Task '{task.title}' is already completed.")
    else:
        task.mark_complete()
        save_projects(projects)
        _info(
            f"Task completed: {task.title} (id={task.id}) in project '{parent.title}'"
        )

    # Show that project’s tasks after update
    print_tasks(
        [(t, parent.id) for t in parent.tasks], projects_by_id={parent.id: parent}
    )


# ------------- Parser Setup ------------- #


def build_parser() -> argparse.ArgumentParser:
    """
    Build and return the argument parser.
    """
    parser = argparse.ArgumentParser(
        prog="project-tracker", description="Command-line Project Management Tool"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # add-user
    p = sub.add_parser("add-user", help="Create a user")
    p.add_argument("--name", required=True, help="User's name")
    p.add_argument("--email", required=False, help="User's email address (optional)")
    p.set_defaults(func=cmd_add_user)

    # list-users
    p = sub.add_parser("list-users", help="List users")
    p.set_defaults(func=cmd_list_users)

    # add-project
    p = sub.add_parser("add-project", help="Create a project for a user")
    p.add_argument("--user", required=True, help="Owner user's name")
    p.add_argument("--title", required=True, help="Project title")
    p.set_defaults(func=cmd_add_project)

    # list-projects
    p = sub.add_parser(
        "list-projects", help="List projects (optionally filter by user)"
    )
    p.add_argument("--user", help="Filter by owner user's name")
    p.set_defaults(func=cmd_list_projects)

    # add-task
    p = sub.add_parser("add-task", help="Add a task to a project")
    p.add_argument("--project", required=True, help="Project title")
    p.add_argument("--title", required=True, help="Task title")
    p.set_defaults(func=cmd_add_task)

    # list-tasks
    p = sub.add_parser("list-tasks", help="List tasks (optionally filter by project)")
    p.add_argument("--project", help="Filter by project title")
    p.set_defaults(func=cmd_list_tasks)

    # complete-task
    p = sub.add_parser("complete-task", help="Mark a task as completed by its ID")
    p.add_argument("--id", required=True, help="Task UUID")
    p.set_defaults(func=cmd_complete_task)

    return parser


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
