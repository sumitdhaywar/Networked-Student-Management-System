from database.connection import mycon


def add_student(id, name, age):
    cur = mycon.cursor()
    query = "INSERT INTO student (id, name, age) VALUES (%s, %s, %s)"
    cur.execute(query, (id, name, age))
    mycon.commit()
    cur.close()
    return "student added successfully"


def get_student(id):
    cur = mycon.cursor()
    query = "SELECT * FROM student WHERE id = %s"
    cur.execute(query, (id,))
    student = cur.fetchone()
    cur.close()
    return student


def get_all_students():
    cur = mycon.cursor()
    query = "SELECT * FROM student"
    cur.execute(query)
    students = cur.fetchall()
    cur.close()
    return students


def update_student(id, name, age):
    cur = mycon.cursor()
    query = "UPDATE student SET name = %s, age = %s WHERE id = %s"
    cur.execute(query, (name, age, id))
    mycon.commit()
    updated = cur.rowcount
    cur.close()
    return updated


def delete_student(id):
    cur = mycon.cursor()
    try:
        cur.execute("DELETE FROM s_data WHERE id = %s", (id,))
        cur.execute(
            "DELETE FROM teacher_student_allocation WHERE student_id = %s",
            (id,),
        )
        cur.execute(
            "DELETE FROM student_course_enrollment WHERE student_id = %s",
            (id,),
        )
        cur.execute(
            "DELETE FROM users WHERE role = 'student' AND reference_id = %s",
            (id,),
        )
        cur.execute("DELETE FROM student WHERE id = %s", (id,))
        deleted = cur.rowcount
        mycon.commit()
    except Exception:
        mycon.rollback()
        raise
    finally:
        cur.close()
    return deleted


def get_student_by_username(username):
    cur = mycon.cursor()
    query = "SELECT id, user_name, password_hash FROM student WHERE user_name = %s"
    cur.execute(query, (username,))
    student = cur.fetchone()
    cur.close()
    return student


def username_exists(username, student_id):
    cur = mycon.cursor()
    query = "SELECT id FROM student WHERE user_name = %s AND id != %s"
    cur.execute(query, (username, student_id))
    student = cur.fetchone()
    cur.close()
    return student is not None


def set_student_credentials(id, username, password_hash):
    cur = mycon.cursor()
    query = "UPDATE student SET user_name = %s, password_hash = %s WHERE id = %s"
    try:
        cur.execute(query, (username, password_hash, id))
        mycon.commit()
        updated = cur.rowcount
    except Exception:
        mycon.rollback()
        raise
    finally:
        cur.close()
    return updated


# Keep old names for backward compatibility
addstudent = add_student
getstudent = get_student
getallstudent = get_all_students
updatestudent = update_student
deletestudent = delete_student
student_username = get_student_by_username
student_username_exists = username_exists
