from database.connection import mycon


def get_user_by_username(username):
    cur = mycon.cursor(dictionary=True)
    query = "SELECT user_id, username, password_hash, role, reference_id FROM users WHERE username = %s"
    cur.execute(query, (username,))
    user = cur.fetchone()
    cur.close()
    return user


def create_user(username, password_hash, role, reference_id=None):
    cur = mycon.cursor()
    query = "INSERT INTO users (username, password_hash, role, reference_id) VALUES (%s, %s, %s, %s)"
    cur.execute(query, (username, password_hash, role, reference_id))
    mycon.commit()
    user_id = cur.lastrowid
    cur.close()
    return user_id


def update_user_password(user_id, password_hash):
    cur = mycon.cursor()
    query = "UPDATE users SET password_hash = %s WHERE user_id = %s"
    cur.execute(query, (password_hash, user_id))
    mycon.commit()
    updated = cur.rowcount
    cur.close()
    return updated


# ===== ADDED: Student Credential Management via users table - START =====


def get_student_user(student_id):
    cur = mycon.cursor(dictionary=True)
    query = (
        "SELECT user_id, username FROM users "
        "WHERE role = 'student' AND reference_id = %s LIMIT 1"
    )
    cur.execute(query, (student_id,))
    user = cur.fetchone()
    cur.close()
    return user


def update_user_credentials(user_id, username, password_hash):
    cur = mycon.cursor()
    query = "UPDATE users SET username = %s, password_hash = %s WHERE user_id = %s"
    try:
        cur.execute(query, (username, password_hash, user_id))
        mycon.commit()
        updated = cur.rowcount
    except Exception:
        mycon.rollback()
        raise
    finally:
        cur.close()
    return updated


# ===== ADDED: Student Credential Management via users table - END =====
