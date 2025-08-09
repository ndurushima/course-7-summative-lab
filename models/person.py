
class Person:
    def __init__(self, name: str, email: str):
        self.name = name.strip()
        self.email = email

    
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, value: str):
        v = value.strip()
        if "@" not in v or "." not in v:
            raise ValueError("Invalid email address")
        self._email = v

# p2 = Person("John Doe", "jd@example.com")
# print(p2.email)

# p1 = Person("Person 1", "qwertyui@pop.com")
# p1.email = "pop@pop.com"
# print(p1.email)  # This will raise ValueError

