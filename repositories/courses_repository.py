from database.connection import mycon


def add_course(co_id, co_name, fees):
    cur = mycon.cursor()
    query = "INSERT INTO course (course_id, course_name, course_fees) VALUES (%s, %s, %s)"
    cur.execute(query, (co_id, co_name, fees))
    mycon.commit()
    cur.close()
    return "course added successfully"


def get_course(co_id):
    cur = mycon.cursor()
    query = "SELECT * FROM course WHERE course_id = %s"
    cur.execute(query, (co_id,))
    course = cur.fetchone()
    cur.close()
    return course


def get_all_courses():
    cur = mycon.cursor()
    query = "SELECT * FROM course"
    cur.execute(query)
    courses = cur.fetchall()
    cur.close()
    return courses


def update_course(co_id, co_name, fees):
    cur = mycon.cursor()
    query = "UPDATE course SET course_name = %s, course_fees = %s WHERE course_id = %s"
    cur.execute(query, (co_name, fees, co_id))
    updated = cur.rowcount
    mycon.commit()
    cur.close()
    return updated


def delete_course(co_id):
    cur = mycon.cursor()
    query = "DELETE FROM course WHERE course_id = %s"
    cur.execute(query, (co_id,))
    deleted = cur.rowcount
    mycon.commit()
    cur.close()
    return deleted


# Keep old names
add_courses = add_course
get_all_course = get_all_courses
