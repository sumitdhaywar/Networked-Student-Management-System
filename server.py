from services import student_services as student_service
from services import auth_services as auth_service
from services import result_services as result_service

# ===== UPDATED: Existing Code - Imports for Teacher, Course and Allocated Student features =====
from services import teacher_services as teacher_service
from services import course_services as course_service
from services import allocation_services as allocation_service
from services import enrollment_services as enrollment_service
from database.connection import mycon

import socket
import threading
import json

# ===== UPDATED: Existing Code - Import date parsing for Teacher Management =====
from datetime import date

HOST = "127.0.0.1"
PORT = 5000
request_lock = threading.Lock()


def send_response(client_socket, response):
    client_socket.sendall(json.dumps(response, default=str).encode())


def get_session_identity(session_token):
    identity = auth_service.verify_session(session_token)
    if not identity or identity.get("success") is False:
        return None
    if isinstance(identity.get("data"), dict):
        identity = identity["data"]
    elif isinstance(identity.get("user"), dict):
        identity = identity["user"]
    return identity


def check_access(session_token, allowed_roles):
    permission = auth_service.check_permission(session_token, allowed_roles)
    if not permission or permission.get("success") is not True:
        return None, permission or {"success": False, "message": "Access denied"}

    identity = get_session_identity(session_token)
    if identity is None:
        return None, {"success": False, "message": "Invalid or expired session"}

    return identity, None


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server listening on {HOST}:{PORT}")

    try:
        while True:
            client_socket, client_address = server.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            thread.start()
    except KeyboardInterrupt:
        print("Server shutting down")
    finally:
        server.close()


def handle_client(client_socket, client_address):
    with request_lock:
        _handle_client_request(client_socket, client_address)


def _handle_client_request(client_socket, client_address):
    try:
        client_socket.settimeout(10)
        print("Client connected:", client_address)

        data = client_socket.recv(1024)
        if not data:
            return

        request_data = json.loads(data.decode())
        request = request_data.get("request")
        payload = request_data.get("data", {})
        session_token = request_data.get("session_token")

        print("Request:", request)

        if request == "Login":
            username = payload.get("username")
            password = payload.get("password")
            response = auth_service.login_user(username, password)

        elif request == "Logout":
            response = auth_service.logout_user(session_token)

        else:
            if request in ("Add_Student", "Display All Student", "update_student", "Delete_Student"):
                allowed_roles = ["admin"]
            elif request == "Add_Marks":
                allowed_roles = ["teacher", "admin"]
            elif request in (
                "Display All Result",
                "Update_Marks",
                "Delete_Marks",
                "result_statistics",
            ):
                # Advanced marks & analytics routes (added for the web frontend)
                allowed_roles = ["admin", "teacher"]
            # ===== ADDED: Teacher Management Feature - START =====
            elif request in (
                "Add_Teacher",
                "Search_Teacher",
                "Display All Teachers",
                "Update_Teacher",
                "Delete_Teacher",
            ):
                allowed_roles = ["admin"]
            # ===== ADDED: Teacher Management Feature - END =====
            # ===== ADDED: Course Management Feature - START =====
            elif request in (
                "Add_Course",
                "Search_Course",
                "Display All Courses",
                "Update_Course",
                "Delete_Course",
            ):
                allowed_roles = ["admin"]
            # ===== ADDED: Course Management Feature - END =====
            # ===== ADDED: Teacher Allocated Students Feature - START =====
            elif request in ("Allocate_Student", "Display All Allocations", "Remove_Allocation"):
                allowed_roles = ["admin"]
            elif request in ("Enroll_Student", "Display All Enrollments", "Remove_Enrollment"):
                allowed_roles = ["admin"]
            elif request == "View_My_Allocated_Students":
                allowed_roles = ["teacher"]
            # ===== ADDED: Teacher Allocated Students Feature - END =====
            # ===== ADDED: Student Login Management Feature - START =====
            elif request == "Set_Student_Credentials":
                allowed_roles = ["admin"]
            # ===== ADDED: Student Login Management Feature - END =====
            elif request in (
                "Search_Student",
                "calculate_result",
                "display_topper",
                "course_toppers",
            ):
                allowed_roles = ["student", "teacher", "admin"]
            else:
                send_response(client_socket, {"success": False, "message": "Invalid request"})
                return

            identity, error = check_access(session_token, allowed_roles)
            if error:
                send_response(client_socket, error)
                return

            role = identity.get("role")
            reference_id = identity.get("reference_id")

            if request == "Add_Student":
                student_id = int(payload.get("id"))
                name = payload.get("name")
                age = int(payload.get("age"))
                response = student_service.add_student_se(student_id, name, age)

            elif request == "Search_Student":
                student_id = int(payload.get("id"))
                if role == "student" and student_id != int(reference_id):
                    response = {"success": False, "message": "You can only view your own details"}
                else:
                    response = student_service.get_student_se(student_id)

            elif request == "Display All Student":
                response = student_service.get_all_student_se()

            elif request == "update_student":
                student_id = int(payload.get("id"))
                name = payload.get("name")
                age = int(payload.get("age"))
                response = student_service.update_student_se(student_id, name, age)

            elif request == "Delete_Student":
                student_id = int(payload.get("id"))
                response = student_service.delete_student_se(student_id)

            elif request == "Add_Marks":
                student_id = int(payload.get("id"))
                co_id = int(payload.get("co_id"))
                t_id = int(payload.get("t_id"))
                marks = float(payload.get("marks"))

                if role == "teacher" and str(reference_id) != str(t_id):
                    response = {"success": False, "message": "access denied: invalid teacher ID"}
                else:
                    response = result_service.add_result_se(student_id, co_id, t_id, marks)

            elif request == "calculate_result":
                student_id = int(payload.get("id"))
                if role == "student" and student_id != int(reference_id):
                    response = {"success": False, "message": "You can only view your own result"}
                else:
                    response = result_service.calculate_result_se(student_id)

            elif request == "display_topper":
                response = result_service.get_topper_se()

            elif request == "course_toppers":
                response = result_service.get_course_toppers_se()

            # --- Advanced marks & result analytics (added for the web frontend) ---
            elif request == "Display All Result":
                response = result_service.get_all_result_se()

            elif request == "result_statistics":
                response = result_service.get_result_statistics_se()

            elif request == "Update_Marks":
                roll = int(payload.get("roll"))
                student_id = int(payload.get("id"))
                co_id = int(payload.get("co_id"))
                t_id = int(payload.get("t_id"))
                marks = float(payload.get("marks"))

                if role == "teacher" and str(reference_id) != str(t_id):
                    response = {"success": False, "message": "access denied: invalid teacher ID"}
                elif role == "teacher":
                    existing = result_service.get_result_se(roll)
                    if not existing.get("success"):
                        response = {"success": False, "message": "result not found"}
                    elif str(existing["data"][3]) != str(reference_id):
                        response = {"success": False, "message": "access denied: not your record"}
                    else:
                        response = result_service.update_result_se(
                            roll, student_id, co_id, t_id, marks
                        )
                else:
                    response = result_service.update_result_se(
                        roll, student_id, co_id, t_id, marks
                    )

            elif request == "Delete_Marks":
                roll = int(payload.get("roll"))

                if role == "teacher":
                    existing = result_service.get_result_se(roll)
                    if not existing.get("success"):
                        response = {"success": False, "message": "result not found"}
                    elif str(existing["data"][3]) != str(reference_id):
                        response = {"success": False, "message": "access denied: not your record"}
                    else:
                        response = result_service.delete_result_se(roll)
                else:
                    response = result_service.delete_result_se(roll)

            # ===== ADDED: Teacher Management Feature - START =====
            elif request == "Add_Teacher":
                t_id = int(payload.get("t_id"))
                t_name = payload.get("t_name")
                j_o_d = date.fromisoformat(str(payload.get("j_o_d")))
                salary = float(payload.get("salary"))
                response = teacher_service.add_teacher_se(t_id, t_name, j_o_d, salary)

            elif request == "Search_Teacher":
                t_id = int(payload.get("t_id"))
                response = teacher_service.get_teacher_se(t_id)

            elif request == "Display All Teachers":
                response = teacher_service.get_all_teacher_se()

            elif request == "Update_Teacher":
                t_id = int(payload.get("t_id"))
                t_name = payload.get("t_name")
                j_o_d = date.fromisoformat(str(payload.get("j_o_d")))
                salary = float(payload.get("salary"))
                response = teacher_service.update_teacher_se(t_id, t_name, j_o_d, salary)

            elif request == "Delete_Teacher":
                t_id = int(payload.get("t_id"))
                response = teacher_service.delete_teacher_se(t_id)
            # ===== ADDED: Teacher Management Feature - END =====

            # ===== ADDED: Course Management Feature - START =====
            elif request == "Add_Course":
                co_id = int(payload.get("co_id"))
                co_name = payload.get("co_name")
                fees = float(payload.get("fees"))
                response = course_service.add_course_se(co_id, co_name, fees)

            elif request == "Search_Course":
                co_id = int(payload.get("co_id"))
                response = course_service.get_course_se(co_id)

            elif request == "Display All Courses":
                response = course_service.get_all_course_se()

            elif request == "Update_Course":
                co_id = int(payload.get("co_id"))
                co_name = payload.get("co_name")
                fees = float(payload.get("fees"))
                response = course_service.update_course_se(co_id, co_name, fees)

            elif request == "Delete_Course":
                co_id = int(payload.get("co_id"))
                response = course_service.delete_course_se(co_id)
            # ===== ADDED: Course Management Feature - END =====

            # ===== ADDED: Teacher Allocated Students Feature - START =====
            elif request == "Allocate_Student":
                response = allocation_service.add_allocation_se(
                    int(payload.get("teacher_id")),
                    int(payload.get("student_id")),
                    int(payload.get("course_id")),
                )

            elif request == "Display All Allocations":
                response = allocation_service.get_all_allocations_se()

            elif request == "Remove_Allocation":
                response = allocation_service.delete_allocation_se(
                    int(payload.get("teacher_id")),
                    int(payload.get("student_id")),
                    int(payload.get("course_id")),
                )

            elif request == "View_My_Allocated_Students":
                # Authorization always uses the verified session reference ID.
                if reference_id is None:
                    response = {
                        "success": False,
                        "message": "account is not linked to a teacher record",
                    }
                else:
                    response = allocation_service.get_allocated_students_se(
                        int(reference_id)
                    )
            # ===== ADDED: Teacher Allocated Students Feature - END =====

            elif request == "Enroll_Student":
                response = enrollment_service.add_enrollment_se(
                    int(payload.get("student_id")),
                    int(payload.get("course_id")),
                )

            elif request == "Display All Enrollments":
                response = enrollment_service.get_all_enrollments_se()

            elif request == "Remove_Enrollment":
                response = enrollment_service.delete_enrollment_se(
                    int(payload.get("student_id")),
                    int(payload.get("course_id")),
                )

            # ===== ADDED: Student Login Management Feature - START =====
            elif request == "Set_Student_Credentials":
                # ===== UPDATED: Existing Code - Store student credentials in the centralized users table =====
                response = auth_service.set_student_login_se(
                    int(payload.get("id")),
                    payload.get("user_name"),
                    payload.get("password"),
                )
            # ===== ADDED: Student Login Management Feature - END =====

            else:
                send_response(client_socket, {"success": False, "message": "Invalid request"})
                return

        send_response(client_socket, response)

    except (ValueError, TypeError):
        send_response(client_socket, {"success": False, "message": "Invalid input data"})
    except Exception as e:
        print("Client error:", e)
        try:
            send_response(client_socket, {"success": False, "message": "Server error"})
        except OSError:
            pass
    finally:
        try:
            if mycon.in_transaction:
                mycon.commit()
        finally:
            client_socket.close()


if __name__ == "__main__":
    start_server()
