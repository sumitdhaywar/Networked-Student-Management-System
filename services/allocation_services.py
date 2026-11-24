from repositories import allocation_repository as repo
from repositories import teacher_repository
from repositories import student_repository
from repositories import courses_repository

def _valid_id(value):
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def add_allocation_se(teacher_id, student_id, course_id):
    if not _valid_id(teacher_id):
        return {"success": False, "message": "invalid teacher id"}
    if not _valid_id(student_id):
        return {"success": False, "message": "invalid student id"}
    if not _valid_id(course_id):
        return {"success": False, "message": "invalid course id"}

    try:
        if teacher_repository.get_teacher(teacher_id) is None:
            return {"success": False, "message": "teacher not found"}
        if student_repository.get_student(student_id) is None:
            return {"success": False, "message": "student not found"}
        if courses_repository.get_course(course_id) is None:
            return {"success": False, "message": "course not found"}
        if repo.get_allocation(teacher_id, student_id, course_id) is not None:
            return {"success": False, "message": "allocation already exists"}

        repo.add_allocation(teacher_id, student_id, course_id)
        return {"success": True, "message": "student allocated successfully"}
    except Exception:
        return {"success": False, "message": "could not add allocation"}


def get_all_allocations_se():
    try:
        allocations = repo.get_all_allocations()
        return {"success": True, "data": allocations}
    except Exception:
        return {"success": False, "message": "failed to get allocations"}


def get_allocated_students_se(teacher_id):
    if not _valid_id(teacher_id):
        return {"success": False, "message": "invalid teacher id"}

    try:
        if teacher_repository.get_teacher(teacher_id) is None:
            return {"success": False, "message": "teacher not found"}
        allocations = repo.get_allocations_for_teacher(teacher_id)
        return {"success": True, "data": allocations}
    except Exception:
        return {"success": False, "message": "failed to get allocated students"}


def delete_allocation_se(teacher_id, student_id, course_id):
    if not _valid_id(teacher_id):
        return {"success": False, "message": "invalid teacher id"}
    if not _valid_id(student_id):
        return {"success": False, "message": "invalid student id"}
    if not _valid_id(course_id):
        return {"success": False, "message": "invalid course id"}

    try:
        if repo.get_allocation(teacher_id, student_id, course_id) is None:
            return {"success": False, "message": "allocation not found"}
        repo.delete_allocation(teacher_id, student_id, course_id)
        return {"success": True, "message": "allocation removed successfully"}
    except Exception:
        return {"success": False, "message": "could not remove allocation"}
