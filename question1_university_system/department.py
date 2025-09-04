from __future__ import annotations
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from .person import Person, Faculty, Professor, Lecturer, TA
from .student import ManagedUndergrad, ManagedGrad


@dataclass
class Course:
    code: str
    title: str
    capacity: int = 50
    prerequisites: List[str] = field(default_factory=list)
    enrolled_students: Set[str] = field(default_factory=set)
    assigned_faculty_id: Optional[str] = None

    def has_seat(self) -> bool:
        return len(self.enrolled_students) < self.capacity

    def assign_faculty(self, faculty_id: str) -> None:
        self.assigned_faculty_id = faculty_id

    def enroll(self, student_id: str) -> None:
        if not self.has_seat():
            raise ValueError(f"Course {self.code} is full")
        self.enrolled_students.add(student_id)

    def drop(self, student_id: str) -> None:
        self.enrolled_students.discard(student_id)


@dataclass
class Department:
    name: str
    faculty: Dict[str, Faculty] = field(default_factory=dict)
    courses: Dict[str, Course] = field(default_factory=dict)
    students: Dict[str, Person] = field(default_factory=dict)

    def add_course(self, course: Course) -> None:
        self.courses[course.code] = course

    def add_faculty(self, member: Faculty) -> None:
        self.faculty[member.id] = member

    def add_student(self, student: Person) -> None:
        self.students[student.id] = student

    def assign_faculty_to_course(self, faculty_id: str, course_code: str) -> None:
        course = self.courses[course_code]
        if faculty_id not in self.faculty:
            raise ValueError("Faculty not in department")
        course.assign_faculty(faculty_id)

    def register_student_for_course(self, student_id: str, course_code: str) -> None:
        course = self.courses[course_code]
        student = self.students[student_id]
        # prerequisite checking (naive): student must already have course codes in record with a grade
        from .student import StudentManagerMixin
        if isinstance(student, StudentManagerMixin):
            missing = [p for p in course.prerequisites if p not in student.record.courses() or student.record.courses()[p] == "IP"]
            if missing:
                raise ValueError(f"Missing prerequisites {missing} for {course_code}")
            course.enroll(student_id)
            student.enroll_course(course_code)
        else:
            raise TypeError("Student does not support managed enrollment")


def demo_polymorphism(people: List[Person]) -> List[str]:
    lines = []
    for p in people:
        lines.append(f"{p.name} -> resp={p.get_responsibilities()}" )
        if hasattr(p, "calculate_workload"):
            lines.append(f"  workload={p.calculate_workload()} hrs/week")
    return lines
