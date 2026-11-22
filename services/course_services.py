from repositories import courses_repository as repo


def add_course_se(co_id, co_name, fees):
    if not isinstance(co_id, int) or isinstance(co_id, bool) or co_id <= 0:
        return {"success": False, "message": "invalid course id"}
    if not isinstance(co_name, str) or not co_name.strip():
        return {"success": False, "message": "course name is not valid"}
    if isinstance(fees, bool) or not isinstance(fees, (int, float)) or fees < 0:
        return {"success": False, "message": "invalid course fees"}
    try:
        repo.add_course(co_id, co_name.strip(), fees)
        return {"success": True, "message": "course added successfully"}
    except Exception as e:
        return {"success": False, "message": str(e)}


def get_course_se(co_id):
    if not isinstance(co_id, int) or isinstance(co_id, bool) or co_id <= 0:
        return {"success": False, "message": "invalid course id"}
    try:
        course = repo.get_course(co_id)
        if course is None:
            return {"success": False, "message": "course not found"}
        return {"success": True, "data": course}
    except Exception:
        return {"success": False, "message": "failed to get course"}


def get_all_course_se():
    try:
        courses = repo.get_all_courses()
        return {"success": True, "data": courses}
    except Exception:
        return {"success": False, "message": "failed to get courses"}


def update_course_se(co_id, co_name, fees):
    if not isinstance(co_id, int) or isinstance(co_id, bool) or co_id <= 0:
        return {"success": False, "message": "invalid course id"}
    if not isinstance(co_name, str) or not co_name.strip():
        return {"success": False, "message": "course name is not valid"}
    if isinstance(fees, bool) or not isinstance(fees, (int, float)) or fees < 0:
        return {"success": False, "message": "invalid course fees"}
    try:
        updated = repo.update_course(co_id, co_name.strip(), fees)
        if updated == 0:
            return {"success": False, "message": "course not found"}
        return {"success": True, "message": "course updated successfully"}
    except Exception:
        return {"success": False, "message": "could not update course"}


def delete_course_se(co_id):
    if not isinstance(co_id, int) or isinstance(co_id, bool) or co_id <= 0:
        return {"success": False, "message": "invalid course id"}
    try:
        deleted = repo.delete_course(co_id)
        if deleted == 0:
            return {"success": False, "message": "course not found"}
        return {"success": True, "message": "deleted successfully"}
    except Exception:
        return {"success": False, "message": "could not delete course"}
