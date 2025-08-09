
from typing import Optional, List, Dict

from models.person import Person
from models.project import Project


class User(Person):
    _ID_COUNTER = 0
    _BY_NAME: Dict[str, int] = {}
    _USERS: Dict[int, "User"] = {}

    def __init__(self, name: str, email: str, id: Optional[int] = None):
        super().__init__(name, email)
        if id is None:
            type(self)._ID_COUNTER += 1
            self.id = type(self)._ID_COUNTER
        else:
            self.id = int(id)
            type(self)._ID_COUNTER = max(type(self)._ID_COUNTER, self.id)
        type(self)._USERS[self.id] = self
        type(self)._BY_NAME[self.name] = self.id
    
    def __repr__(self) -> str:
        return f"User(id={self.id}, name='{self.name}', email='{self.email}')"

    @property
    def projects(self) -> List["Project"]:
        return [p for p in Project.all() if p.user_id == self.id]
    
    @classmethod
    def get(cls, name: str) -> Optional["User"]:
        for user in cls.all():
            if user.name == name:
                return user
        return None
    
    @classmethod
    def all(cls) -> List["User"]:
        return [u for u in cls._USERS.values() if isinstance(u, cls)] 
    
    @classmethod
    def create(cls, name: str, email: str) -> "User":
        if cls.get(name):
            raise ValueError(f"User with name '{name}' already exists.")
        user = cls(name=name, email=email)
        cls._USERS[user.id] = user
        return user
    
    @classmethod
    def clear_all(cls):
        cls._USERS.clear()
        cls._BY_NAME.clear()
        cls._ID_COUNTER = 0

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }
    @classmethod
    def from_dict(cls, data: Dict) -> "User":
        return cls(name=data["name"], email=data["email"], id=data.get("id"))   

