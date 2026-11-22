from repositories import courses_repository
from repositories import enrollment_repository as repo
from repositories import student_repository


def _valid_id(value):
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def add_enrollment_se(student_id, course_id):
    if not _valid_id(student_id):
        return {"success": False, "message": "invalid student id"}
    if not _valid_id(course_id):
        return {"success": False, "message": "invalid course id"}

    try:
        if student_repository.get_student(student_id) is None:
            return {"success": False, "message": "student not found"}
        if courses_repository.get_course(course_id) is None:
            return {"success": False, "message": "course not found"}
        if repo.get_enrollment(student_id, course_id) is not None:
            return {"success": False, "message": "student is already enrolled in this course"}

        repo.add_enrollment(student_id, course_id)
        return {"success": True, "message": "student enrolled successfully"}
    except Exception:
        return {"success": False, "message": "could not enroll student"}


def get_all_enrollments_se():
    try:
        return {"success": True, "data": repo.get_all_enrollments()}
    except Exception:
        return {"success": False, "message": "failed to get course enrollments"}


def delete_enrollment_se(student_id, course_id):
    if not _valid_id(student_id):
        return {"success": False, "message": "invalid student id"}
    if not _valid_id(course_id):
        return {"success": False, "message": "invalid course id"}

    try:
        if repo.get_enrollment(student_id, course_id) is None:
            return {"success": False, "message": "enrollment not found"}
        repo.delete_enrollment(student_id, course_id)
        return {"success": True, "message": "enrollment removed successfully"}
    except Exception:
        return {"success": False, "message": "could not remove enrollment"}
