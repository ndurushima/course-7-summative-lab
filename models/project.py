from typing import Optional, List, Dict
from models.task import Task
from datetime import datetime


class Project:
    _PROJECTS: Dict[int, "Project"] = {}

    def __init__(self, title: str, description: str, user_id: int, due_date: str, id: Optional[int] = None):
        self.user_id = int(user_id)
        self.title = title.strip()
        self.description = description.strip()
        self.due_date = due_date
        if id is None:
            self.id = (max(type(self)._PROJECTS.keys()) + 1) if type(self)._PROJECTS else 1
        else:
            self.id = int(id)
        type(self)._PROJECTS[self.id] = self
    

    @property
    def due_date(self) -> str:
        return self._due_date
    
    @due_date.setter
    def due_date(self, value: str):
        dt = datetime.strptime(value.strip(), "%Y-%m-%d")
        self._due_date = dt.date().isoformat()


    @property
    def tasks(self) -> List["Task"]:
        return [t for t in Task.all() if t.project_id == self.id]
    
    def add_task(self, title: str, status: str, assigned_to: Optional[int] = None) -> "Task":
        return Task.create(project_id=self.id, title=title, status=status, assigned_to=assigned_to)
    
    @classmethod
    def create(cls, user_id: int, title: str, description: str, due_date: str) -> "Project":
        return cls(title, description, user_id, due_date, id=None)

    @classmethod
    def get(cls, id: int) -> Optional["Project"]:
        return cls._PROJECTS.get(id)
    
    @classmethod
    def all(cls) -> List["Project"]:
        return list(cls._PROJECTS.values())
    
