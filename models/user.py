
from typing import Optional, List

from models.person import Person
from models.project import Project


class User(Person):
    _ID_COUNTER = 0

    def __init__(self, name: str, email: str, id: Optional[int] = None):
        super().__init__(name, email)
        if id is None:
            type(self)._ID_COUNTER += 1
            self.id = type(self)._ID_COUNTER
        else:
            self.id = int(id)
    
    @property
    def projects(self) -> List["Project"]:
        return [p for p in Project.all() if p.user_id == self.id]
    
    def create_project(self, title: str, description: str, due_date: str) -> "Project":
        return Project.create(user_id=self.id, title=title, description=description, due_date=due_date)
    

