from database.connection import mycon


def add_enrollment(student_id, course_id):
    cur = mycon.cursor()
    query = (
        "INSERT INTO student_course_enrollment (student_id, course_id) "
        "VALUES (%s, %s)"
    )
    try:
        cur.execute(query, (student_id, course_id))
        mycon.commit()
        inserted = cur.rowcount
    except Exception:
        mycon.rollback()
        raise
    finally:
        cur.close()
    return inserted


def get_enrollment(student_id, course_id):
    cur = mycon.cursor()
    query = (
        "SELECT student_id, course_id FROM student_course_enrollment "
        "WHERE student_id = %s AND course_id = %s"
    )
    cur.execute(query, (student_id, course_id))
    enrollment = cur.fetchone()
    cur.close()
    return enrollment


def get_all_enrollments():
    cur = mycon.cursor()
    query = """SELECT s.id, s.name, c.course_id, c.course_name
               FROM student_course_enrollment e
               JOIN student s ON s.id = e.student_id
               JOIN course c ON c.course_id = e.course_id
               ORDER BY c.course_id, s.id"""
    cur.execute(query)
    enrollments = cur.fetchall()
    cur.close()
    return enrollments


def delete_enrollment(student_id, course_id):
    cur = mycon.cursor()
    query = (
        "DELETE FROM student_course_enrollment "
        "WHERE student_id = %s AND course_id = %s"
    )
    try:
        cur.execute(query, (student_id, course_id))
        mycon.commit()
        deleted = cur.rowcount
    except Exception:
        mycon.rollback()
        raise
    finally:
        cur.close()
    return deleted
