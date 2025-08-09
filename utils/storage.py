import json, os
from json import JSONDecodeError
from models.user import User
from models.project import Project
from models.task import Task

DB_PATH = "data/storage.json"

def load():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(DB_PATH):
        return
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            db = json.load(f)
    except (JSONDecodeError, ValueError):
        db = {}
    
    if not isinstance(db, list):
        db = {"users": db, "projects": [], "tasks": []}
    elif not isinstance(db, dict):
        db = {}

    # reset registries
    if hasattr(User, "clear_all"): User.clear_all()
    if hasattr(Project, "clear_all"): Project.clear_all()
    if hasattr(Task, "clear_all"): Task.clear_all()

    for u in db.get("users", []):
        User.from_dict(u)
    for p in db.get("projects", []):
        Project.from_dict(p)
    for t in db.get("tasks", []):
        Task.from_dict(t)

def save():
    os.makedirs("data", exist_ok=True)
    db = {
        "users":    [u.to_dict() for u in User.all()],
        "projects": [p.to_dict() for p in Project.all()],
        "tasks":    [t.to_dict() for t in Task.all()],
    }
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)