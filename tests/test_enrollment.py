import random
from unittest.mock import patch

from services import course_services as course_service
from services import enrollment_services as enrollment_service
from services import student_services as student_service


def test_enrollment_service_validation_and_repository_calls():
    student_id = 123
    course_id = 456
    with patch.object(
        enrollment_service.student_repository,
        "get_student",
        return_value=(student_id,),
    ), patch.object(
        enrollment_service.courses_repository,
        "get_course",
        return_value=(course_id,),
    ), patch.object(
        enrollment_service.repo, "get_enrollment", return_value=None
    ), patch.object(enrollment_service.repo, "add_enrollment") as add_enrollment:
        result = enrollment_service.add_enrollment_se(student_id, course_id)
        assert result["success"] is True
        add_enrollment.assert_called_once_with(student_id, course_id)

    with patch.object(
        enrollment_service.student_repository, "get_student"
    ) as get_student, patch.object(
        enrollment_service.repo, "add_enrollment"
    ) as add_enrollment:
        result = enrollment_service.add_enrollment_se(0, course_id)
        assert result["success"] is False
        get_student.assert_not_called()
        add_enrollment.assert_not_called()

    with patch.object(
        enrollment_service.student_repository,
        "get_student",
        return_value=(student_id,),
    ), patch.object(
        enrollment_service.courses_repository,
        "get_course",
        return_value=(course_id,),
    ), patch.object(
        enrollment_service.repo,
        "get_enrollment",
        return_value=(student_id, course_id),
    ), patch.object(enrollment_service.repo, "add_enrollment") as add_enrollment:
        result = enrollment_service.add_enrollment_se(student_id, course_id)
        assert result["success"] is False
        add_enrollment.assert_not_called()


def test_enrollment_list_and_remove_service():
    student_id = 123
    course_id = 456
    expected = [(student_id, "Asha", course_id, "Math")]
    with patch.object(
        enrollment_service.repo, "get_all_enrollments", return_value=expected
    ):
        result = enrollment_service.get_all_enrollments_se()
        assert result == {"success": True, "data": expected}

    with patch.object(
        enrollment_service.repo,
        "get_enrollment",
        return_value=(student_id, course_id),
    ), patch.object(
        enrollment_service.repo, "delete_enrollment"
    ) as delete_enrollment:
        result = enrollment_service.delete_enrollment_se(student_id, course_id)
        assert result["success"] is True
        delete_enrollment.assert_called_once_with(student_id, course_id)


def test_student_course_enrollment():
    student_id = random.randint(100000, 900000)
    course_id = random.randint(100000, 900000)

    student_result = student_service.add_student_se(
        student_id, "test_enroll_student", 20
    )
    assert student_result["success"] is True, "add student failed"

    course_result = course_service.add_course_se(
        course_id, "test_enroll_course", 15000
    )
    assert course_result["success"] is True, "add course failed"

    try:
        result = enrollment_service.add_enrollment_se(student_id, course_id)
        assert result["success"] is True, "enroll student failed"

        result = enrollment_service.add_enrollment_se(student_id, course_id)
        assert result["success"] is False, "duplicate enrollment was allowed"

        result = enrollment_service.get_all_enrollments_se()
        assert result["success"] is True, "listing enrollments failed"
        assert any(
            row[0] == student_id and row[2] == course_id for row in result["data"]
        ), "enrollment not present in course roster"

        result = enrollment_service.delete_enrollment_se(student_id, course_id)
        assert result["success"] is True, "remove enrollment failed"

        result = enrollment_service.delete_enrollment_se(student_id, course_id)
        assert result["success"] is False, "missing enrollment was removed"

        result = enrollment_service.add_enrollment_se(-1, course_id)
        assert result["success"] is False, "invalid student id was accepted"
    finally:
        enrollment_service.delete_enrollment_se(student_id, course_id)
        course_service.delete_course_se(course_id)
        student_service.delete_student_se(student_id)
