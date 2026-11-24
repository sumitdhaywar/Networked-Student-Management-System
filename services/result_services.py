import math

from repositories import result_repository as repo


def add_result_se(id, co_id, t_id, marks):
    if not isinstance(id, int) or isinstance(id, bool) or id <= 0:
        return {"success": False, "message": "invalid student id"}
    if not isinstance(co_id, int) or isinstance(co_id, bool) or co_id <= 0:
        return {"success": False, "message": "invalid course id"}
    if not isinstance(t_id, int) or isinstance(t_id, bool) or t_id <= 0:
        return {"success": False, "message": "invalid teacher id"}
    if (
        isinstance(marks, bool)
        or not isinstance(marks, (int, float))
        or marks < 0
        or marks > 100
        or not math.isfinite(marks)
    ):
        return {"success": False, "message": "invalid marks"}
    try:
        roll = repo.add_result(id, co_id, t_id, marks)
        return {"success": True, "message": "result added successfully", "roll": roll}
    except Exception as e:
        return {"success": False, "message": str(e)}


def get_result_se(roll):
    if not isinstance(roll, int) or isinstance(roll, bool) or roll <= 0:
        return {"success": False, "message": "invalid roll"}
    try:
        result = repo.get_result(roll)
        if result is None:
            return {"success": False, "message": "result not found"}
        return {"success": True, "data": result}
    except Exception:
        return {"success": False, "message": "failed to get result"}


def get_all_result_se():
    try:
        results = repo.get_all_results()
        return {"success": True, "data": results}
    except Exception:
        return {"success": False, "message": "failed to get results"}


def update_result_se(roll, id, co_id, t_id, marks):
    if not isinstance(roll, int) or isinstance(roll, bool) or roll <= 0:
        return {"success": False, "message": "invalid roll"}
    if not isinstance(id, int) or isinstance(id, bool) or id <= 0:
        return {"success": False, "message": "invalid student id"}
    if not isinstance(co_id, int) or isinstance(co_id, bool) or co_id <= 0:
        return {"success": False, "message": "invalid course id"}
    if not isinstance(t_id, int) or isinstance(t_id, bool) or t_id <= 0:
        return {"success": False, "message": "invalid teacher id"}
    if (
        isinstance(marks, bool)
        or not isinstance(marks, (int, float))
        or marks < 0
        or marks > 100
        or not math.isfinite(marks)
    ):
        return {"success": False, "message": "invalid marks"}
    try:
        updated = repo.update_result(roll, id, co_id, t_id, marks)
        if updated == 0:
            return {"success": False, "message": "result not found"}
        return {"success": True, "message": "result updated successfully"}
    except Exception:
        return {"success": False, "message": "could not update result"}


def delete_result_se(roll):
    if not isinstance(roll, int) or isinstance(roll, bool) or roll <= 0:
        return {"success": False, "message": "invalid roll"}
    try:
        deleted = repo.delete_result(roll)
        if deleted == 0:
            return {"success": False, "message": "result not found"}
        return {"success": True, "message": "deleted successfully"}
    except Exception:
        return {"success": False, "message": "could not delete result"}


def calculate_result_se(id):
    if not isinstance(id, int) or isinstance(id, bool) or id <= 0:
        return {"success": False, "message": "invalid student id"}

    try:
        results = repo.get_student_marks(id)
        marks = [row[0] for row in results if row[0] is not None]
        if not marks:
            return {"success": False, "message": "no marks found"}

        total = sum(marks)
        percentage = total / len(marks)
        status = "Pass" if all(mark >= 35 for mark in marks) else "Fail"

        return {
            "success": True,
            "message": "result calculated successfully",
            "total": total,
            "percentage": round(percentage, 2),
            "status": status
        }
    except Exception as e:
        return {"success": False, "message": str(e)}


def get_topper_se():
    try:
        topper = repo.get_topper()
        if topper is None or topper[2] is None or topper[3] is None:
            return {"success": False, "message": "topper not found"}
        return {"success": True, "data": topper}
    except Exception as e:
        return {"success": False, "message": str(e)}


def get_course_toppers_se():
    try:
        rows = repo.get_course_topper_rows()
    except Exception:
        return {"success": False, "message": "failed to get course toppers"}

    courses = []
    current_course_id = None
    for row in rows:
        course_id, course_name, student_id, student_name, total, average = row
        if course_id != current_course_id:
            courses.append({
                "course_id": course_id,
                "course_name": course_name,
                "topper": None,
            })
            current_course_id = course_id

        if (
            student_id is not None
            and total is not None
            and average is not None
            and courses[-1]["topper"] is None
        ):
            courses[-1]["topper"] = {
                "id": student_id,
                "name": student_name,
                "total": float(total),
                "average": round(float(average), 2),
            }

    return {"success": True, "data": courses}


def get_result_statistics_se():
    try:
        rows = repo.get_result_statistics_rows()
    except Exception as e:
        return {"success": False, "message": str(e)}

    if not rows:
        return {"success": False, "message": "no results found"}

    students = []
    for row in rows:
        student_id, name, subjects, total, average, failed_subjects = row
        if not subjects or total is None or average is None:
            continue
        failed_subjects = int(failed_subjects or 0)
        students.append({
            "id": student_id,
            "name": name,
            "subjects": int(subjects),
            "total": float(total),
            "average": round(float(average), 2),
            "failed_subjects": failed_subjects,
            "status": "Pass" if failed_subjects == 0 else "Fail"
        })

    if not students:
        return {"success": False, "message": "no results found"}

    class_average = round(
        sum(student["average"] for student in students) / len(students), 2
    )
    highest = max(students, key=lambda student: student["average"])
    lowest = min(students, key=lambda student: student["average"])
    passed = sum(1 for student in students if student["status"] == "Pass")

    return {
        "success": True,
        "data": {
            "students_with_results": len(students),
            "class_average": class_average,
            "highest": highest,
            "lowest": lowest,
            "passed": passed,
            "failed": len(students) - passed
        }
    }


get_result_statistics_service = get_result_statistics_se
