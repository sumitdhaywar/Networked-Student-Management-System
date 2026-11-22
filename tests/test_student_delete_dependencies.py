from datetime import date
import random

from database.connection import mycon
from services import allocation_services
from services import auth_services
from services import course_services
from services import enrollment_services
from services import result_services
from services import student_services
from services import teacher_services


def test_delete_student_removes_dependent_records():
    student_id = random.randint(10000000, 99999999)
    teacher_id = random.randint(10000000, 99999999)
    course_id = random.randint(10000000, 99999999)
    username = f"s{student_id}"

    try:
        assert student_services.add_student_se(
            student_id, "DeleteStudent", 18
        )["success"]
        assert teacher_services.add_teacher_se(
            teacher_id, "DeleteTeacher", date(2020, 1, 1), 1000
        )["success"]
        assert course_services.add_course_se(
            course_id, "DeleteCourse", 1000
        )["success"]
        assert result_services.add_result_se(
            student_id, course_id, teacher_id, 85
        )["success"]
        assert allocation_services.add_allocation_se(
            teacher_id, student_id, course_id
        )["success"]
        assert enrollment_services.add_enrollment_se(
            student_id, course_id
        )["success"]
        assert auth_services.set_student_login_se(
            student_id, username, "TestStudent@123"
        )["success"]

        result = student_services.delete_student_se(student_id)
        assert result["success"], result

        cur = mycon.cursor()
        checks = (
            ("student", "SELECT COUNT(*) FROM student WHERE id = %s"),
            ("marks", "SELECT COUNT(*) FROM s_data WHERE id = %s"),
            (
                "allocation",
                "SELECT COUNT(*) FROM teacher_student_allocation WHERE student_id = %s",
            ),
            (
                "enrollment",
                "SELECT COUNT(*) FROM student_course_enrollment WHERE student_id = %s",
            ),
            (
                "student account",
                "SELECT COUNT(*) FROM users WHERE role = 'student' AND reference_id = %s",
            ),
        )
        for label, query in checks:
            cur.execute(query, (student_id,))
            assert cur.fetchone()[0] == 0, f"{label} remained after student deletion"
        cur.close()
    finally:
        student_services.delete_student_se(student_id)
        teacher_services.delete_teacher_se(teacher_id)
        course_services.delete_course_se(course_id)
