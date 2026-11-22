from database.connection import mycon


def add_result(id, co_id, t_id, marks):
    cur = mycon.cursor()
    query = "INSERT INTO s_data (id, course_id, teacher_id, marks) VALUES (%s, %s, %s, %s)"
    cur.execute(query, (id, co_id, t_id, marks))
    roll = cur.lastrowid
    mycon.commit()
    cur.close()
    return roll


def get_result(roll):
    cur = mycon.cursor()
    query = "SELECT * FROM s_data WHERE roll = %s"
    cur.execute(query, (roll,))
    result = cur.fetchone()
    cur.close()
    return result


def get_all_results():
    cur = mycon.cursor()
    query = "SELECT * FROM s_data"
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    return results


def update_result(roll, id, co_id, t_id, marks):
    cur = mycon.cursor()
    query = "UPDATE s_data SET id = %s, course_id = %s, teacher_id = %s, marks = %s WHERE roll = %s"
    cur.execute(query, (id, co_id, t_id, marks, roll))
    updated = cur.rowcount
    mycon.commit()
    cur.close()
    return updated


def delete_result(roll):
    cur = mycon.cursor()
    query = "DELETE FROM s_data WHERE roll = %s"
    cur.execute(query, (roll,))
    deleted = cur.rowcount
    mycon.commit()
    cur.close()
    return deleted


def get_student_marks(id):
    cur = mycon.cursor()
    query = "SELECT marks FROM s_data WHERE id = %s"
    cur.execute(query, (id,))
    results = cur.fetchall()
    cur.close()
    return results


def get_topper():
    cur = mycon.cursor()
    query = """SELECT s.id, s.name, SUM(d.marks), AVG(d.marks)
               FROM student s
               JOIN s_data d ON s.id = d.id
               GROUP BY s.id, s.name
               ORDER BY AVG(d.marks) DESC
               LIMIT 1"""
    cur.execute(query)
    topper = cur.fetchone()
    cur.close()
    return topper


def get_course_topper_rows():
    cur = mycon.cursor()
    query = """SELECT c.course_id, c.course_name, s.id, s.name,
                      SUM(d.marks), AVG(d.marks)
               FROM course c
               LEFT JOIN s_data d ON d.course_id = c.course_id
               LEFT JOIN student s ON s.id = d.id
               GROUP BY c.course_id, c.course_name, s.id, s.name
               ORDER BY c.course_id, AVG(d.marks) DESC, s.id"""
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    return rows


# Advanced analytics (added for the web frontend - non-destructive addition)
def get_result_statistics_rows():
    cur = mycon.cursor()
    query = """SELECT s.id, s.name, COUNT(d.marks), SUM(d.marks), AVG(d.marks),
                      SUM(CASE WHEN d.marks < 35 THEN 1 ELSE 0 END)
               FROM student s
               JOIN s_data d ON s.id = d.id
               GROUP BY s.id, s.name"""
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    return rows


# Keep old names
get_all_result = get_all_results


