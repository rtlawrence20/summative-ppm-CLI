from utils import storage


def test_save_and_load_users(make_user):
    users = [make_user("Alex", "alex@example.com"), make_user("Bri", "bri@example.com")]
    storage.save_users(users)
    loaded = storage.load_users()
    assert len(loaded) == 2
    assert {u.email for u in loaded} == {"alex@example.com", "bri@example.com"}


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
    users = [make_user("Alex", "alex@example.com"), make_user("Bri", "bri@example.com")]
    storage.save_users(users)
    projects = [make_project("Alpha", users[0].id), make_project("Bravo", users[1].id)]
    storage.save_projects(projects)

    u = storage.get_user_by_name(storage.load_users(), "alex")
    assert u and u.email == "alex@example.com"

    p = storage.get_project_by_title(storage.load_projects(), "bravo")
    assert p and p.title == "Bravo"

    idx = storage.index_by_id(storage.load_projects())
    assert projects[0].id in idx and projects[1].id in idx
