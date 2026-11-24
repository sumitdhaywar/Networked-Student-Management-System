import math
from datetime import date

from repositories import teacher_repository as repo


def add_teacher_se(t_id, t_name, j_o_d, sal):
    if not isinstance(t_id, int) or isinstance(t_id, bool) or t_id <= 0:
        return {"success": False, "message": "invalid teacher id"}
    if not isinstance(t_name, str) or not t_name.strip() or len(t_name.strip()) > 30:
        return {"success": False, "message": "teacher name is not valid"}
    if not isinstance(j_o_d, date):
        return {"success": False, "message": "invalid joining date"}
    if (
        isinstance(sal, bool)
        or not isinstance(sal, (int, float))
        or sal < 0
        or sal > 99999999.99
        or not math.isfinite(sal)
    ):
        return {"success": False, "message": "invalid salary"}
    try:
        repo.add_teacher(t_id, t_name.strip(), j_o_d, sal)
        return {"success": True, "message": "teacher added successfully"}
    except Exception as e:
        return {"success": False, "message": str(e)}


def get_teacher_se(t_id):
    if not isinstance(t_id, int) or isinstance(t_id, bool) or t_id <= 0:
        return {"success": False, "message": "invalid teacher id"}
    try:
        teacher = repo.get_teacher(t_id)
        if teacher is None:
            return {"success": False, "message": "teacher not found"}
        return {"success": True, "data": teacher}
    except Exception:
        return {"success": False, "message": "failed to get teacher"}


def get_all_teacher_se():
    try:
        teachers = repo.get_all_teachers()
        return {"success": True, "data": teachers}
    except Exception:
        return {"success": False, "message": "failed to get teachers"}


def update_teacher_se(t_id, t_name, j_o_d, sal):
    if not isinstance(t_id, int) or isinstance(t_id, bool) or t_id <= 0:
        return {"success": False, "message": "invalid teacher id"}
    if not isinstance(t_name, str) or not t_name.strip() or len(t_name.strip()) > 30:
        return {"success": False, "message": "teacher name is not valid"}
    if not isinstance(j_o_d, date):
        return {"success": False, "message": "invalid joining date"}
    if (
        isinstance(sal, bool)
        or not isinstance(sal, (int, float))
        or sal < 0
        or sal > 99999999.99
        or not math.isfinite(sal)
    ):
        return {"success": False, "message": "invalid salary"}
    try:
        updated = repo.update_teacher(t_id, t_name.strip(), j_o_d, sal)
        if updated == 0:
            return {"success": False, "message": "teacher not found"}
        return {"success": True, "message": "teacher updated successfully"}
    except Exception:
        return {"success": False, "message": "could not update teacher"}


def delete_teacher_se(t_id):
    if not isinstance(t_id, int) or isinstance(t_id, bool) or t_id <= 0:
        return {"success": False, "message": "invalid teacher id"}
    try:
        deleted = repo.delete_teacher(t_id)
        if deleted == 0:
            return {"success": False, "message": "teacher not found"}
        return {"success": True, "message": "deleted successfully"}
    except Exception:
        return {"success": False, "message": "could not delete teacher"}
