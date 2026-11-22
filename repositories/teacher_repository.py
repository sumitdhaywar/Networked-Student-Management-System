from database.connection import mycon


def add_teacher(t_id, t_name, j_o_d, salary):
    cur = mycon.cursor()
    query = "INSERT INTO teacher (teacher_id, teacher_name, salary, j_o_d) VALUES (%s, %s, %s, %s)"
    cur.execute(query, (t_id, t_name, salary, j_o_d))
    mycon.commit()
    cur.close()
    return "teacher added successfully"


def get_teacher(t_id):
    cur = mycon.cursor()
    query = "SELECT * FROM teacher WHERE teacher_id = %s"
    cur.execute(query, (t_id,))
    teacher = cur.fetchone()
    cur.close()
    return teacher


def get_all_teachers():
    cur = mycon.cursor()
    query = "SELECT * FROM teacher"
    cur.execute(query)
    teachers = cur.fetchall()
    cur.close()
    return teachers


def update_teacher(t_id, t_name, j_o_d, salary):
    cur = mycon.cursor()
    query = "UPDATE teacher SET teacher_name = %s, j_o_d = %s, salary = %s WHERE teacher_id = %s"
    cur.execute(query, (t_name, j_o_d, salary, t_id))
    updated = cur.rowcount
    mycon.commit()
    cur.close()
    return updated


def delete_teacher(t_id):
    cur = mycon.cursor()
    query = "DELETE FROM teacher WHERE teacher_id = %s"
    cur.execute(query, (t_id,))
    deleted = cur.rowcount
    mycon.commit()
    cur.close()
    return deleted


# Keep old names
get_all_teacher = get_all_teachers
