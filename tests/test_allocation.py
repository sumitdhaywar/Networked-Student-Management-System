from datetime import date

import random

from services import allocation_services as ser
from services import teacher_services as teacher_ser
from services import student_services as student_ser
from services import course_services as course_ser

# ===== ADDED: Teacher Allocated Students Feature - tests =====


def test_allocation():
    teacher_id = random.randint(100000, 900000)
    student_id = random.randint(100000, 900000)
    course_id = random.randint(100000, 900000)

    result = teacher_ser.add_teacher_se(
        teacher_id, "test_alloc_teacher", date(2021, 6, 1), 50000
    )
    assert result["success"] is True, "add teacher failed"

    result = student_ser.add_student_se(student_id, "test_alloc_student", 20)
    assert result["success"] is True, "add student failed"

    result = course_ser.add_course_se(course_id, "test_alloc_course", 15000)
    assert result["success"] is True, "add course failed"

    try:
        result = ser.add_allocation_se(teacher_id, student_id, course_id)
        assert result["success"] is True, "add allocation failed"

        result = ser.add_allocation_se(teacher_id, student_id, course_id)
        assert result["success"] is False, "duplicate allocation was allowed"

        result = ser.get_all_allocations_se()
        assert result["success"] is True, "listing all allocations failed"
        assert any(
            row[0] == student_id and row[2] == course_id and row[4] == teacher_id
            for row in result["data"]
        ), "allocation not present in all allocations"

        result = ser.get_allocated_students_se(teacher_id)
        assert result["success"] is True, "listing teacher allocations failed"
        assert any(
            row[0] == student_id and row[2] == course_id for row in result["data"]
        ), "allocation not present for teacher"

        result = ser.delete_allocation_se(teacher_id, student_id, course_id)
        assert result["success"] is True, "remove allocation failed"

        result = ser.delete_allocation_se(teacher_id, student_id, course_id)
        assert result["success"] is False, "missing allocation was removed"

        result = ser.add_allocation_se(-1, student_id, course_id)
        assert result["success"] is False, "invalid teacher id was accepted"
    finally:
        ser.delete_allocation_se(teacher_id, student_id, course_id)
        course_ser.delete_course_se(course_id)
        student_ser.delete_student_se(student_id)
        teacher_ser.delete_teacher_se(teacher_id)

    print("all allocation operations passed")


# ===== ADDED: Teacher Allocated Students Feature - tests END =====
