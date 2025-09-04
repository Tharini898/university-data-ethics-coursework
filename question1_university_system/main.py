from question1_university_system.person import Professor, Lecturer, TA
from question1_university_system.student import ManagedUndergrad, ManagedGrad
from question1_university_system.department import Department, Course, demo_polymorphism


def build_demo():
    cs = Department(name="Computer Science")
    # Faculty
    prof = Professor("F001", "Ada Lovelace", "ada@uni.edu", department="CS")
    lec  = Lecturer("F002", "Grace Hopper", "grace@uni.edu", department="CS")
    ta   = TA("F003", "Linus Torvalds", "linus@uni.edu", department="CS")

    for f in (prof, lec, ta):
        cs.add_faculty(f)

    # Courses
    cs.add_course(Course(code="CS101", title="Intro to CS", capacity=3))
    cs.add_course(Course(code="CS201", title="Data Structures", capacity=2, prerequisites=["CS101"]))

    cs.assign_faculty_to_course(prof.id, "CS101")
    cs.assign_faculty_to_course(lec.id, "CS201")

    # Students
    s1 = ManagedUndergrad("S001", "john doe", "john@uni.edu")
    s2 = ManagedUndergrad("S002", "jane smith", "jane@uni.edu")
    s3 = ManagedGrad("S003", "sara connor", "sara@uni.edu")
    for s in (s1, s2, s3):
        cs.add_student(s)

    # Enrollments
    cs.register_student_for_course("S001", "CS101")
    cs.register_student_for_course("S002", "CS101")
    cs.register_student_for_course("S003", "CS101")

    # Finish CS101 with grades, then try CS201 which requires CS101
    s1.record.set_grade("CS101", "A")
    s2.record.set_grade("CS101", "B+")
    s3.record.set_grade("CS101", "A-")

    cs.register_student_for_course("S001", "CS201")
    cs.register_student_for_course("S002", "CS201")
    # Next one would raise capacity error if uncommented:
    # cs.register_student_for_course("S003", "CS201")  # capacity=2

    # GPA & statuses
    print("-- GPA & Status --")
    for s in (s1, s2, s3):
        print(s.name, s.record.courses(), "GPA:", s.calculate_gpa(), "Status:", s.get_academic_status())

    # Polymorphism demo
    print("\n-- Polymorphism --")
    for line in demo_polymorphism([prof, lec, ta, s1, s2, s3]):
        print(line)


if __name__ == "__main__":
    build_demo()
