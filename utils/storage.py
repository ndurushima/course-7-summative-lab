import json, os
from models.user import User
from models.project import Project
from models.task import Task

DB_PATH = "data/storage.json"

def load():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(DB_PATH):
        return
    with open(DB_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)

    # reset registries
    if hasattr(User, "clear"): User.clear()
    if hasattr(Project, "clear"): Project.clear()
    if hasattr(Task, "clear"): Task.clear()

    for u in db.get("users", []):
        User.from_dict(u)
    for p in db.get("projects", []):
        Project.from_dict(p)
    for t in db.get("tasks", []):
        Task.from_dict(t)

def save():
    db = {
        "users":   [u.to_dict()   for u in (User.all()    if hasattr(User, "all") else [])],
        "projects":[p.to_dict()   for p in (Project.all() if hasattr(Project, "all") else [])],
        "tasks":   [t.to_dict()   for t in (Task.all()    if hasattr(Task, "all") else [])],
    }
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)