from repositories import student_repository as repo
import hashlib
import secrets
import hmac


def add_student_se(id, name, age):
    if not isinstance(id, int) or isinstance(id, bool) or id <= 0:
        return {"success": False, "message": "invalid student id"}

    if not isinstance(name, str) or not name.strip():
        return {"success": False, "message": "invalid student name"}

    if not isinstance(age, int) or isinstance(age, bool) or age <= 0:
        return {"success": False, "message": "invalid student age"}

    try:
        repo.add_student(id, name.strip(), age)
        return {"success": True, "message": "student added successfully"}
    except Exception as e:
        return {"success": False, "message": str(e)}


def get_student_se(id):
    if not isinstance(id, int) or isinstance(id, bool) or id <= 0:
        return {"success": False, "message": "id is invalid"}

    try:
        student = repo.get_student(id)
        if student is None:
            return {"success": False, "message": "student not found"}
        return {"success": True, "data": student}
    except Exception as e:
        return {"success": False, "message": str(e)}


def get_all_student_se():
    try:
        students = repo.get_all_students()
        return {"success": True, "data": students}
    except Exception as e:
        return {"success": False, "message": str(e)}


def update_student_se(id, name, age):
    if not isinstance(id, int) or isinstance(id, bool) or id <= 0:
        return {"success": False, "message": "id is invalid"}

    if not isinstance(name, str) or not name.strip():
        return {"success": False, "message": "name cannot be empty"}

    if not isinstance(age, int) or isinstance(age, bool) or age <= 0:
        return {"success": False, "message": "invalid age"}

    try:
        updated = repo.update_student(id, name.strip(), age)
        if updated == 0:
            return {"success": False, "message": "student not found"}
        return {"success": True, "message": "updated successfully"}
    except Exception as e:
        return {"success": False, "message": str(e)}


def delete_student_se(id):
    if not isinstance(id, int) or isinstance(id, bool) or id <= 0:
        return {"success": False, "message": "id is invalid"}

    try:
        deleted = repo.delete_student(id)
        if deleted == 0:
            return {"success": False, "message": "student not found"}
        return {"success": True, "message": "deleted successfully"}
    except Exception as e:
        return {"success": False, "message": str(e)}


def set_student_credentials_se(id, user_name, password):
    if not isinstance(id, int) or isinstance(id, bool) or id <= 0:
        return {"success": False, "message": "invalid student id"}

    if not isinstance(user_name, str) or not user_name.strip() or len(user_name.strip()) > 20:
        return {"success": False, "message": "invalid username"}

    if not isinstance(password, str) or len(password) < 8:
        return {"success": False, "message": "password must contain at least 8 characters"}

    try:
        user_name = user_name.strip()
        if repo.username_exists(user_name, id):
            return {"success": False, "message": "username already exists"}

        salt = secrets.token_bytes(16)
        password_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200000)
        stored_hash = salt.hex() + "$" + password_hash.hex()

        updated = repo.set_student_credentials(id, user_name, stored_hash)
        if updated == 0:
            return {"success": False, "message": "student not found"}

        return {"success": True, "message": "student credentials created successfully"}
    except Exception as e:
        return {"success": False, "message": str(e)}


def login_student_se(user_name, password):
    if not isinstance(user_name, str) or not user_name.strip():
        return {"success": False, "message": "invalid username"}

    if not isinstance(password, str) or not password:
        return {"success": False, "message": "invalid password"}

    try:
        student = repo.get_student_by_username(user_name.strip())
        if student is None:
            return {"success": False, "message": "invalid username or password"}

        salt_hex, stored_hash = student[2].split("$")
        salt = bytes.fromhex(salt_hex)
        password_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200000)

        if not hmac.compare_digest(password_hash.hex(), stored_hash):
            return {"success": False, "message": "invalid username or password"}

        return {
            "success": True,
            "message": "login successful",
            "student_id": student[0],
            "user_name": student[1]
        }
    except Exception:
        return {"success": False, "message": "login failed"}


# Keep old names
add_student_service = add_student_se
get_student_service = get_student_se
get_all_student_service = get_all_student_se
update_student_service = update_student_se
delete_student_service = delete_student_se
set_student_credentials_service = set_student_credentials_se
login_student_service = login_student_se

