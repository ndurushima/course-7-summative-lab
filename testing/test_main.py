import pytest
import sys
from main import main
from models.user import User
from models.project import Project
from models.task import Task


@pytest.fixture(autouse=True)


def run_cli(args):
    """Helper to invoke your CLI like: run_cli(['add-user', 'Name', 'email'])"""
    sys.argv = ["main.py"] + args
    main()

def test_add_project(capsys):
    # Arrange: user exists
    run_cli(["add-user", "Nathan", "n@example.com"])
    # Act
    run_cli(["add-project", "Nathan", "Code", "Add tests", "2025-08-09"])
    out = capsys.readouterr().out
    assert "Project created" in out

    # Assert: project belongs to user and fields are correct
    u = User.get_by_name("Nathan")
    assert u is not None
    assert len(u.projects) == 1
    p = u.projects[0]
    assert p.title == "Code"
    assert p.description == "Add tests"
    assert p.due_date == "2025-08-09"


def test_add_task(capsys):
    run_cli(["add-user", "Nathan", "n@example.com"])
    run_cli(["add-project", "Nathan", "Code", "Add tests", "2025-08-09"])
    run_cli(["add-task", "Nathan", "1", "Write unit tests", "todo"])
    out = capsys.readouterr().out
    assert "Task created" in out

    p = Project.get(1)
    assert p is not None
    assert len(p.tasks) == 1
    t = p.tasks[0]
    assert t.title == "Write unit tests"
    assert t.status == "todo"
    assert t.assigned_to == User.get_by_name("Nathan").id


