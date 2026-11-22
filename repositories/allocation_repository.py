from database.connection import mycon

# ===== ADDED: Teacher Allocated Students Feature - START =====


def add_allocation(teacher_id, student_id, course_id):
    cur = mycon.cursor()
    query = (
        "INSERT INTO teacher_student_allocation (teacher_id, student_id, course_id) "
        "VALUES (%s, %s, %s)"
    )
    try:
        cur.execute(query, (teacher_id, student_id, course_id))
        mycon.commit()
        inserted = cur.rowcount
    except Exception:
        mycon.rollback()
        raise
    finally:
        cur.close()
    return inserted


def get_allocation(teacher_id, student_id, course_id):
    cur = mycon.cursor()
    query = (
        "SELECT teacher_id, student_id, course_id FROM teacher_student_allocation "
        "WHERE teacher_id = %s AND student_id = %s AND course_id = %s"
    )
    cur.execute(query, (teacher_id, student_id, course_id))
    allocation = cur.fetchone()
    cur.close()
    return allocation


def get_all_allocations():
    cur = mycon.cursor()
    query = """SELECT s.id, s.name, c.course_id, c.course_name, t.teacher_id, t.teacher_name
               FROM teacher_student_allocation a
               JOIN student s ON s.id = a.student_id
               JOIN course c ON c.course_id = a.course_id
               JOIN teacher t ON t.teacher_id = a.teacher_id
               ORDER BY t.teacher_id, s.id, c.course_id"""
    cur.execute(query)
    allocations = cur.fetchall()
    cur.close()
    return allocations


def get_allocations_for_teacher(teacher_id):
    cur = mycon.cursor()
    query = """SELECT s.id, s.name, c.course_id, c.course_name, t.teacher_id, t.teacher_name
               FROM teacher_student_allocation a
               JOIN student s ON s.id = a.student_id
               JOIN course c ON c.course_id = a.course_id
               JOIN teacher t ON t.teacher_id = a.teacher_id
               WHERE a.teacher_id = %s
               ORDER BY s.id, c.course_id"""
    cur.execute(query, (teacher_id,))
    allocations = cur.fetchall()
    cur.close()
    return allocations


def delete_allocation(teacher_id, student_id, course_id):
    cur = mycon.cursor()
    query = (
        "DELETE FROM teacher_student_allocation "
        "WHERE teacher_id = %s AND student_id = %s AND course_id = %s"
    )
    try:
        cur.execute(query, (teacher_id, student_id, course_id))
        mycon.commit()
        deleted = cur.rowcount
    except Exception:
        mycon.rollback()
        raise
    finally:
        cur.close()
    return deleted


# ===== ADDED: Teacher Allocated Students Feature - END =====
