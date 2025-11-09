import json


def run(argv):
    from main import main

    main(argv)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_cli_add_user_project_task_complete(tmp_path, isolate_storage_paths):
    users_path = isolate_storage_paths.USERS_PATH
    projects_path = isolate_storage_paths.PROJECTS_PATH

    # add-user (with email)
    run(["add-user", "--name", "Alex", "--email", "alex@example.com"])
    users = read_json(users_path)
    assert len(users) == 1
    assert users[0]["name"] == "Alex"
    assert users[0]["email"] == "alex@example.com"

    # add-project for Alex
    run(["add-project", "--user", "Alex", "--title", "CLI Tool"])
    projects = read_json(projects_path)
    assert len(projects) == 1
    assert projects[0]["title"] == "CLI Tool"
    assert projects[0]["tasks"] == []

    # add-task to project
    run(["add-task", "--project", "CLI Tool", "--title", "Implement add-task"])
    projects = read_json(projects_path)
    assert len(projects[0]["tasks"]) == 1
    task_id = projects[0]["tasks"][0]["id"]
    assert projects[0]["tasks"][0]["title"] == "Implement add-task"
    assert projects[0]["tasks"][0]["status"] == "todo"

    # complete-task
    run(["complete-task", "--id", task_id])
    projects = read_json(projects_path)
    assert projects[0]["tasks"][0]["status"] == "done"


def test_cli_list_commands_do_not_crash(isolate_storage_paths, capsys):
    # Verifies list commands run with empty data without exceptions
    run(["list-users"])
    run(["list-projects"])
    run(["list-tasks"])
    captured = capsys.readouterr()
    assert captured.out is not None or captured.err is not None
