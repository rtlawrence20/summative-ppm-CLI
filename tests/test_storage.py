from utils import storage


def test_save_and_load_users(make_user):
    users = [make_user("Alex", None), make_user("Bri", None)]
    storage.save_users(users)
    loaded = storage.load_users()
    assert len(loaded) == 2
    # Emails are optional; we created both with None above.
    assert {u.email for u in loaded} == {None}
    # Sanity check: names round-trip correctly.
    assert {u.name for u in loaded} == {"Alex", "Bri"}


def test_save_and_load_projects(make_project):
    p1 = make_project(title="CLI Tool", user_id="u1", with_tasks=True)
    p2 = make_project(title="Web App", user_id="u1", with_tasks=False)
    storage.save_projects([p1, p2])
    loaded = storage.load_projects()
    assert len(loaded) == 2
    tcounts = {p.title: len(p.tasks) for p in loaded}
    assert tcounts["CLI Tool"] == 2
    assert tcounts["Web App"] == 0


def test_lookup_helpers(make_user, make_project):
    users = [make_user("Alex", None), make_user("Bri", None)]
    storage.save_users(users)
    projects = [make_project("Alpha", users[0].id), make_project("Bravo", users[1].id)]
    storage.save_projects(projects)

    u = storage.get_user_by_name(storage.load_users(), "alex")
    assert u and u.name == "Alex"

    p = storage.get_project_by_title(storage.load_projects(), "bravo")
    assert p and p.title == "Bravo"

    idx = storage.index_by_id(storage.load_projects())
    assert projects[0].id in idx and projects[1].id in idx
