from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional


class Person(ABC):
    """Base person with validated properties and polymorphic hooks."""

    def __init__(self, person_id: str, name: str, email: str):
        self._id = None
        self._name = None
        self._email = None
        self.id = person_id
        self.name = name
        self.email = email

    # Encapsulated attributes with validation
    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        if not value or not isinstance(value, str):
            raise ValueError("id must be a non-empty string")
        self._id = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not value or not isinstance(value, str):
            raise ValueError("name must be a non-empty string")
        self._name = value.title()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        if "@" not in value:
            raise ValueError("email must contain '@'")
        self._email = value.lower()

    @abstractmethod
    def get_responsibilities(self) -> List[str]:
        """Return role-specific responsibilities (polymorphic)."""
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, name={self.name!r})"


class Staff(Person):
    def get_responsibilities(self) -> List[str]:
        return ["Administrative support", "Operations", "Student services"]


class Student(Person):
    def __init__(self, person_id: str, name: str, email: str, level: str):
        super().__init__(person_id, name, email)
        self.level = level  # Undergraduate or Graduate

    def get_responsibilities(self) -> List[str]:
        return ["Attend classes", "Complete assignments", "Maintain academic integrity"]


class Faculty(Person, ABC):
    def __init__(self, person_id: str, name: str, email: str, department: str):
        super().__init__(person_id, name, email)
        self.department = department

    @abstractmethod
    def calculate_workload(self) -> int:
        """Return teaching + research + service load in hours per week."""
        ...


class Professor(Faculty):
    def get_responsibilities(self) -> List[str]:
        return ["Teach courses", "Research & publish", "Supervise students", "Service"]

    def calculate_workload(self) -> int:
        return 12  # heuristic


class Lecturer(Faculty):
    def get_responsibilities(self) -> List[str]:
        return ["Teach courses", "Develop curricula", "Advise students"]

    def calculate_workload(self) -> int:
        return 16


class TA(Faculty):
    def get_responsibilities(self) -> List[str]:
        return ["Assist teaching", "Grade assignments", "Hold office hours"]

    def calculate_workload(self) -> int:
        return 10


class UndergraduateStudent(Student):
    def __init__(self, person_id: str, name: str, email: str):
        super().__init__(person_id, name, email, level="Undergraduate")


class GraduateStudent(Student):
    def __init__(self, person_id: str, name: str, email: str):
        super().__init__(person_id, name, email, level="Graduate")
