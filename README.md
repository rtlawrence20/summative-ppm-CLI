# Project Management CLI

A Python **command-line interface (CLI)** for managing users, projects, and tasks — with formatting and persistent local storage.  
This tool simulates a multi-user project tracker.

---

## Features

- **User Management** — Create and list users (email now optional)
- **Project Management** — Create projects and assign them to users
- **Task Management** — Add, list, and complete tasks
- **Data Persistence** — All data is saved locally as JSON files
- **Clean CLI Output** — Uses `__str__` methods for readable display
- **Rich Formatting** — Uses [Rich](https://pypi.org/project/rich/) for pretty tables (auto-disables if not installed)
- **Automated Tests** — Fully tested with `pytest`

---

## Installation

1. Clone this repository:

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

Run commands from the project root:

### Add a User
```bash
python -m main add-user --name "Alex"
```
> Email is optional: `--email "alex@example.com"` may be included if desired.

### Add a Project
```bash
python -m main add-project --user "Alex" --title "CLI Tool"
```

### Add a Task
```bash
python -m main add-task --project "CLI Tool" --title "Implement add-task"
```

### Mark a Task Complete
```bash
python -m main complete-task --id <task_id>
```

### List Users
```bash
python -m main list-users
```

### List Projects
```bash
python -m main list-projects
```

### List Tasks
```bash
python -m main list-tasks
```

---

## Project Structure

```
.
├── main.py
├── models/
│   ├── user.py
│   ├── project.py
│   └── task.py
├── utils/
│   ├── storage.py
│   └── formatting.py
├── tests/
│   ├── test_cli.py
│   ├── test_models.py
│   ├── test_storage.py
│   ├── test_formatting.py
│   └── conftest.py
├── requirements.txt
└── README.md
```

---

## Data Persistence

All records are saved in JSON format within the project directory:

```
data/
├── users.json
├── projects.json
└── tasks.json
```

Files are auto-created and updated on each operation.  
The app loads and saves seamlessly using the `storage.py` utility.

---

## Testing

Run the full test suite:
```bash
pytest -v
```

---

## Dependencies

| Package | Purpose | PyPI Link |
|----------|----------|------------|
| **rich** | Optional terminal formatting | [pypi.org/project/rich](https://pypi.org/project/rich) |
| **pytest** | Test framework | [pypi.org/project/pytest](https://pypi.org/project/pytest) |

---

## 🏁 Example Output

Example listing after adding users and projects:

```
ID                                   Name     Email        Created At
----------------------------------   -------  -----------  -------------------------
e1c9f8b2-8a3b-4f59-b9b7-8b04f1d56d7  Alex     -            2025-11-08T19:22:04+00:00
c8b032cb-7214-4ebf-9075-6375b5d6c874  Bri      -            2025-11-08T19:22:12+00:00
```
