from typing import Optional, List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from models.project import Project

class Task:
    _TASKS: Dict[int, "Task"] = {}

    def __init__(self, project_id: int, title: str, status: str, assigned_to: Optional[int] = None, id: Optional[int] = None):
        self.project_id = int(project_id)
        self.title = title.strip()
        self.status = status
        self.assigned_to = assigned_to

        self.id = int(id) if id is not None else (max(self._TASKS.keys()) + 1 if self._TASKS else 1)
        type(self)._TASKS[self.id] = self

    
    @classmethod
    def create(cls, title: str, project_id: int, status: str, assigned_to: Optional[int] = None) -> "Task":
        from models.project import Project
        if not Project.get(project_id):
            raise ValueError("Project does not exist")
        return cls(project_id=project_id, title=title, status=status, assigned_to=assigned_to)
    
    @classmethod
    def get(cls, id: int) -> Optional["Task"]:
        return cls._TASKS.get(id)
    
    @classmethod
    def all(cls) -> List["Task"]:
        return list(cls._TASKS.values())
    
    @classmethod
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "project_id": self.project_id,
            "title": self.title,
            "status": self.status,
            "assigned_to": self.assigned_to
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Task":
        return cls(
            id=data.get("id"),
            project_id=data.get("project_id"),
            title=data.get("title"),
            status=data.get("status"),
            assigned_to=data.get("assigned_to")
        )