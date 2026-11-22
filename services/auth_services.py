import hashlib
import hmac
import secrets
import time

from repositories import auth_repository as repo

# ===== UPDATED: Existing Code - Student lookup for login credential creation =====
from repositories import student_repository

sessions = {}
SESSION_TIMEOUT = 1800


def login_user(username, password):
    if not isinstance(username, str) or not username.strip():
        return {"success": False, "message": "invalid username"}

    if not isinstance(password, str) or not password:
        return {"success": False, "message": "invalid password"}

    try:
        user = repo.get_user_by_username(username.strip())
        if user is None:
            return {"success": False, "message": "invalid username or password"}

        salt_hex, stored_hash = user["password_hash"].split("$")
        salt = bytes.fromhex(salt_hex)
        password_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200000)

        if not hmac.compare_digest(password_hash.hex(), stored_hash):
            return {"success": False, "message": "invalid username or password"}

        session_token = secrets.token_urlsafe(32)
        sessions[session_token] = {
            "user_id": user["user_id"],
            "username": user["username"],
            "role": user["role"],
            "reference_id": user["reference_id"],
            "created_at": time.time()
        }

        return {
            "success": True,
            "message": "login successful",
            "session_token": session_token,
            "user_id": user["user_id"],
            "username": user["username"],
            "role": user["role"],
            "reference_id": user["reference_id"]
        }
    except Exception:
        return {"success": False, "message": "login failed"}


def verify_session(session_token):
    if not isinstance(session_token, str) or not session_token:
        return {"success": False, "message": "invalid session"}

    session = sessions.get(session_token)
    if session is None:
        return {"success": False, "message": "session not found"}

    if time.time() - session["created_at"] > SESSION_TIMEOUT:
        sessions.pop(session_token, None)
        return {"success": False, "message": "session expired"}

    return {
        "success": True,
        "message": "valid session",
        "user_id": session["user_id"],
        "username": session["username"],
        "role": session["role"],
        "reference_id": session["reference_id"]
    }


def logout_user(session_token):
    if not isinstance(session_token, str) or not session_token:
        return {"success": False, "message": "invalid session"}

    if session_token not in sessions:
        return {"success": False, "message": "session not found"}

    sessions.pop(session_token, None)
    return {"success": True, "message": "logout successful"}


def change_password(username, old_password, new_password):
    if not username or not isinstance(username, str):
        return {"success": False, "message": "invalid username"}

    if not isinstance(old_password, str) or not old_password:
        return {"success": False, "message": "invalid old password"}

    if not isinstance(new_password, str) or len(new_password) < 8:
        return {"success": False, "message": "new password must contain at least 8 characters"}

    try:
        user = repo.get_user_by_username(username.strip())
        if user is None:
            return {"success": False, "message": "invalid username or password"}

        salt_hex, stored_hash = user["password_hash"].split("$")
        salt = bytes.fromhex(salt_hex)
        old_hash = hashlib.pbkdf2_hmac("sha256", old_password.encode(), salt, 200000)

        if not hmac.compare_digest(old_hash.hex(), stored_hash):
            return {"success": False, "message": "invalid username or password"}

        new_salt = secrets.token_bytes(16)
        new_hash = hashlib.pbkdf2_hmac("sha256", new_password.encode(), new_salt, 200000)
        stored_new_hash = new_salt.hex() + "$" + new_hash.hex()

        updated = repo.update_user_password(user["user_id"], stored_new_hash)
        if updated == 0:
            return {"success": False, "message": "password not updated"}

        return {"success": True, "message": "password changed successfully"}
    except Exception:
        return {"success": False, "message": "password change failed"}


def set_initial_password(username, new_password):
    if not isinstance(username, str) or not username.strip():
        return {"success": False, "message": "invalid username"}

    if not isinstance(new_password, str) or len(new_password) < 8:
        return {"success": False, "message": "password must contain at least 8 characters"}

    try:
        user = repo.get_user_by_username(username.strip())
        if user is None:
            return {"success": False, "message": "user not found"}

        if user["role"] not in ("student", "teacher", "admin"):
            return {"success": False, "message": "not allowed for this account"}

        salt = secrets.token_bytes(16)
        password_hash = hashlib.pbkdf2_hmac("sha256", new_password.encode(), salt, 200000)
        stored_hash = salt.hex() + "$" + password_hash.hex()

        updated = repo.update_user_password(user["user_id"], stored_hash)
        if updated == 0:
            return {"success": False, "message": "password not updated"}

        return {"success": True, "message": "initial password created successfully"}
    except Exception:
        return {"success": False, "message": "password setup failed"}


# ===== ADDED: Student Credential Management via users table - START =====
def set_student_login_se(student_id, user_name, password):
    if not isinstance(student_id, int) or isinstance(student_id, bool) or student_id <= 0:
        return {"success": False, "message": "invalid student id"}

    if (
        not isinstance(user_name, str)
        or not user_name.strip()
        or len(user_name.strip()) > 20
    ):
        return {"success": False, "message": "invalid username"}

    if not isinstance(password, str) or len(password) < 8:
        return {"success": False, "message": "password must contain at least 8 characters"}

    try:
        if student_repository.get_student(student_id) is None:
            return {"success": False, "message": "student not found"}

        user_name = user_name.strip()
        existing_by_name = repo.get_user_by_username(user_name)
        existing_student = repo.get_student_user(student_id)

        if existing_by_name is not None and (
            existing_student is None
            or existing_by_name["user_id"] != existing_student["user_id"]
        ):
            return {"success": False, "message": "username already exists"}

        salt = secrets.token_bytes(16)
        password_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200000)
        stored_hash = salt.hex() + "$" + password_hash.hex()

        if existing_student is not None:
            updated = repo.update_user_credentials(
                existing_student["user_id"], user_name, stored_hash
            )
            if updated == 0:
                return {"success": False, "message": "could not update student credentials"}
            return {"success": True, "message": "student credentials updated successfully"}

        repo.create_user(user_name, stored_hash, "student", student_id)
        return {"success": True, "message": "student credentials created successfully"}
    except Exception:
        return {"success": False, "message": "could not save student credentials"}
# ===== ADDED: Student Credential Management via users table - END =====


def check_permission(session_token, allowed_roles):
    session_result = verify_session(session_token)
    if not session_result.get("success"):
        return {"success": False, "message": "authentication required"}

    if session_result.get("role") not in allowed_roles:
        return {"success": False, "message": "access denied"}

    return {"success": True, "message": "access granted", "user": session_result}
