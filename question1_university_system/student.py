from __future__ import annotations
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from .person import Student, UndergraduateStudent, GraduateStudent


@dataclass
class SecureStudentRecord:
    """Encapsulated student record with validation and limits."""
    max_enrollments: int = 6
    _gpa_history: Dict[str, float] = field(default_factory=dict)  # semester -> GPA
    _courses: Dict[str, str] = field(default_factory=dict)  # course_code -> grade or "IP"

    def set_semester_gpa(self, semester: str, gpa: float) -> None:
        if not (0.0 <= gpa <= 4.0):
            raise ValueError("GPA must be between 0.0 and 4.0")
        self._gpa_history[semester] = round(gpa, 2)

    def get_semester_gpa(self, semester: str) -> Optional[float]:
        return self._gpa_history.get(semester)

    def enroll(self, course_code: str) -> None:
        if course_code in self._courses:
            raise ValueError(f"Already enrolled in {course_code}")
        if len(self._courses) >= self.max_enrollments:
            raise ValueError("Enrollment limit reached")
        self._courses[course_code] = "IP"  # In Progress

    def drop(self, course_code: str) -> None:
        if course_code not in self._courses:
            raise ValueError(f"Not enrolled in {course_code}")
        del self._courses[course_code]

    def set_grade(self, course_code: str, letter: str) -> None:
        if course_code not in self._courses:
            raise ValueError("Course not found in record")
        if letter not in {"A", "A-", "B+", "B", "B-", "C+", "C", "D", "F"}:
            raise ValueError("Invalid letter grade")
        self._courses[course_code] = letter

    def courses(self) -> Dict[str, str]:
        return dict(self._courses)


class StudentManagerMixin:
    """Mixin adding enrollment & GPA logic to Student."""
    def __init__(self):
        self.record = SecureStudentRecord()

    def enroll_course(self, course_code: str) -> None:
        self.record.enroll(course_code)

    def drop_course(self, course_code: str) -> None:
        self.record.drop(course_code)

    def calculate_gpa(self) -> float:
        # Simple 4.0 scale mapping for completed courses; IP are ignored
        weights = {"A":4.0,"A-":3.7,"B+":3.3,"B":3.0,"B-":2.7,"C+":2.3,"C":2.0,"D":1.0,"F":0.0}
        grades = [weights[g] for g in self.record.courses().values() if g != "IP"]
        return round(sum(grades)/len(grades), 2) if grades else 0.0

    def get_academic_status(self) -> str:
        gpa = self.calculate_gpa()
        if gpa >= 3.7: return "Dean's List"
        if gpa < 2.0:  return "Probation"
        return "Good Standing"


class ManagedUndergrad(UndergraduateStudent, StudentManagerMixin):
    def __init__(self, person_id: str, name: str, email: str):
        UndergraduateStudent.__init__(self, person_id, name, email)
        StudentManagerMixin.__init__(self)


class ManagedGrad(GraduateStudent, StudentManagerMixin):
    def __init__(self, person_id: str, name: str, email: str):
        GraduateStudent.__init__(self, person_id, name, email)
        StudentManagerMixin.__init__(self)
