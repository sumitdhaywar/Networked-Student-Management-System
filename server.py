import json
import socket
import threading
from datetime import date

from database.connection import mycon
from services import allocation_services as allocation_service
from services import auth_services as auth_service
from services import course_services as course_service
from services import enrollment_services as enrollment_service
from services import result_services as result_service
from services import student_services as student_service
from services import teacher_services as teacher_service

HOST = "127.0.0.1"
PORT = 5000
request_lock = threading.Lock()
MAX_REQUEST_BYTES = 1024 * 1024


def send_response(client_socket, response):
    client_socket.sendall(json.dumps(response, default=str).encode())


def parse_integer(payload, field):
    value = payload.get(field)
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise ValueError(f"{field} must be an integer")
    return int(value)


def parse_number(payload, field):
    value = payload.get(field)
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise ValueError(f"{field} must be numeric")
    return float(value)


def receive_request(client_socket):
    """Read one complete JSON object, tolerating split TCP packets."""
    data = bytearray()
    while True:
        chunk = client_socket.recv(min(4096, MAX_REQUEST_BYTES + 1 - len(data)))
        if not chunk:
            break
        data.extend(chunk)
        if len(data) > MAX_REQUEST_BYTES:
            raise ValueError("Request is too large")

        if b"\n" in data:
            request_line, _, trailing = data.partition(b"\n")
            if trailing.strip():
                raise ValueError("Multiple requests are not supported")
            return json.loads(request_line.decode("utf-8"))

        try:
            return json.loads(data.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue

    if not data:
        return None
    return json.loads(data.decode("utf-8"))


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


def teacher_owns_result(result, teacher_id):
    """Check the teacher id stored in the fourth column of an s_data row."""
    return result.get("success") and str(result["data"][3]) == str(teacher_id)


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

        request_data = receive_request(client_socket)
        if request_data is None:
            return

        if not isinstance(request_data, dict):
            send_response(
                client_socket,
                {"success": False, "message": "Request must be a JSON object"},
            )
            return

        request = request_data.get("request")
        payload = request_data.get("data", {})
        if not isinstance(request, str) or not isinstance(payload, dict):
            send_response(
                client_socket,
                {"success": False, "message": "Invalid request data"},
            )
            return
        session_token = request_data.get("session_token")

        print("Request:", request)

        # Login and Logout manage the session itself, so they run before access checks.
        if request == "Login":
            username = payload.get("username")
            password = payload.get("password")
            response = auth_service.login_user(username, password)

        elif request == "Logout":
            response = auth_service.logout_user(session_token)

        else:
            if request in (
                "Add_Student",
                "Display All Student",
                "update_student",
                "Delete_Student",
            ):
                allowed_roles = ["admin"]
            elif request == "Add_Marks":
                allowed_roles = ["teacher", "admin"]
            elif request in (
                "Display All Result",
                "Update_Marks",
                "Delete_Marks",
                "result_statistics",
            ):
                allowed_roles = ["admin", "teacher"]
            elif request in (
                "Add_Teacher",
                "Search_Teacher",
                "Display All Teachers",
                "Update_Teacher",
                "Delete_Teacher",
            ):
                allowed_roles = ["admin"]
            elif request in (
                "Add_Course",
                "Search_Course",
                "Display All Courses",
                "Update_Course",
                "Delete_Course",
            ):
                allowed_roles = ["admin"]
            elif request in ("Allocate_Student", "Display All Allocations", "Remove_Allocation"):
                allowed_roles = ["admin"]
            elif request in ("Enroll_Student", "Display All Enrollments", "Remove_Enrollment"):
                allowed_roles = ["admin"]
            elif request == "View_My_Allocated_Students":
                allowed_roles = ["teacher"]
            elif request == "Set_Student_Credentials":
                allowed_roles = ["admin"]
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
                student_id = parse_integer(payload, "id")
                name = payload.get("name")
                age = parse_integer(payload, "age")
                response = student_service.add_student_se(student_id, name, age)

            elif request == "Search_Student":
                student_id = parse_integer(payload, "id")
                if role == "student" and student_id != int(reference_id):
                    response = {"success": False, "message": "You can only view your own details"}
                else:
                    response = student_service.get_student_se(student_id)

            elif request == "Display All Student":
                response = student_service.get_all_student_se()

            elif request == "update_student":
                student_id = parse_integer(payload, "id")
                name = payload.get("name")
                age = parse_integer(payload, "age")
                response = student_service.update_student_se(student_id, name, age)

            elif request == "Delete_Student":
                student_id = parse_integer(payload, "id")
                response = student_service.delete_student_se(student_id)

            elif request == "Add_Marks":
                student_id = parse_integer(payload, "id")
                course_id = parse_integer(payload, "co_id")
                teacher_id = parse_integer(payload, "t_id")
                marks = parse_number(payload, "marks")

                if role == "teacher" and str(reference_id) != str(teacher_id):
                    response = {"success": False, "message": "access denied: invalid teacher ID"}
                else:
                    response = result_service.add_result_se(
                        student_id, course_id, teacher_id, marks
                    )

            elif request == "calculate_result":
                student_id = parse_integer(payload, "id")
                if role == "student" and student_id != int(reference_id):
                    response = {"success": False, "message": "You can only view your own result"}
                else:
                    response = result_service.calculate_result_se(student_id)

            elif request == "display_topper":
                response = result_service.get_topper_se()

            elif request == "course_toppers":
                response = result_service.get_course_toppers_se()

            elif request == "Display All Result":
                response = result_service.get_all_result_se()

            elif request == "result_statistics":
                response = result_service.get_result_statistics_se()

            elif request == "Update_Marks":
                roll = parse_integer(payload, "roll")
                student_id = parse_integer(payload, "id")
                course_id = parse_integer(payload, "co_id")
                teacher_id = parse_integer(payload, "t_id")
                marks = parse_number(payload, "marks")

                if role == "teacher" and str(reference_id) != str(teacher_id):
                    response = {"success": False, "message": "access denied: invalid teacher ID"}
                elif role == "teacher":
                    existing = result_service.get_result_se(roll)
                    if not existing.get("success"):
                        response = {"success": False, "message": "result not found"}
                    elif not teacher_owns_result(existing, reference_id):
                        response = {"success": False, "message": "access denied: not your record"}
                    else:
                        response = result_service.update_result_se(
                            roll, student_id, course_id, teacher_id, marks
                        )
                else:
                    response = result_service.update_result_se(
                        roll, student_id, course_id, teacher_id, marks
                    )

            elif request == "Delete_Marks":
                roll = parse_integer(payload, "roll")

                if role == "teacher":
                    existing = result_service.get_result_se(roll)
                    if not existing.get("success"):
                        response = {"success": False, "message": "result not found"}
                    elif not teacher_owns_result(existing, reference_id):
                        response = {"success": False, "message": "access denied: not your record"}
                    else:
                        response = result_service.delete_result_se(roll)
                else:
                    response = result_service.delete_result_se(roll)

            elif request == "Add_Teacher":
                teacher_id = parse_integer(payload, "t_id")
                teacher_name = payload.get("t_name")
                joining_date = date.fromisoformat(str(payload.get("j_o_d")))
                salary = parse_number(payload, "salary")
                response = teacher_service.add_teacher_se(
                    teacher_id, teacher_name, joining_date, salary
                )

            elif request == "Search_Teacher":
                teacher_id = parse_integer(payload, "t_id")
                response = teacher_service.get_teacher_se(teacher_id)

            elif request == "Display All Teachers":
                response = teacher_service.get_all_teacher_se()

            elif request == "Update_Teacher":
                teacher_id = parse_integer(payload, "t_id")
                teacher_name = payload.get("t_name")
                joining_date = date.fromisoformat(str(payload.get("j_o_d")))
                salary = parse_number(payload, "salary")
                response = teacher_service.update_teacher_se(
                    teacher_id, teacher_name, joining_date, salary
                )

            elif request == "Delete_Teacher":
                teacher_id = parse_integer(payload, "t_id")
                response = teacher_service.delete_teacher_se(teacher_id)

            elif request == "Add_Course":
                course_id = parse_integer(payload, "co_id")
                course_name = payload.get("co_name")
                fees = parse_number(payload, "fees")
                response = course_service.add_course_se(course_id, course_name, fees)

            elif request == "Search_Course":
                course_id = parse_integer(payload, "co_id")
                response = course_service.get_course_se(course_id)

            elif request == "Display All Courses":
                response = course_service.get_all_course_se()

            elif request == "Update_Course":
                course_id = parse_integer(payload, "co_id")
                course_name = payload.get("co_name")
                fees = parse_number(payload, "fees")
                response = course_service.update_course_se(course_id, course_name, fees)

            elif request == "Delete_Course":
                course_id = parse_integer(payload, "co_id")
                response = course_service.delete_course_se(course_id)

            elif request == "Allocate_Student":
                response = allocation_service.add_allocation_se(
                    parse_integer(payload, "teacher_id"),
                    parse_integer(payload, "student_id"),
                    parse_integer(payload, "course_id"),
                )

            elif request == "Display All Allocations":
                response = allocation_service.get_all_allocations_se()

            elif request == "Remove_Allocation":
                response = allocation_service.delete_allocation_se(
                    parse_integer(payload, "teacher_id"),
                    parse_integer(payload, "student_id"),
                    parse_integer(payload, "course_id"),
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

            elif request == "Enroll_Student":
                response = enrollment_service.add_enrollment_se(
                    parse_integer(payload, "student_id"),
                    parse_integer(payload, "course_id"),
                )

            elif request == "Display All Enrollments":
                response = enrollment_service.get_all_enrollments_se()

            elif request == "Remove_Enrollment":
                response = enrollment_service.delete_enrollment_se(
                    parse_integer(payload, "student_id"),
                    parse_integer(payload, "course_id"),
                )

            elif request == "Set_Student_Credentials":
                response = auth_service.set_student_login_se(
                    parse_integer(payload, "id"),
                    payload.get("user_name"),
                    payload.get("password"),
                )

            else:
                send_response(client_socket, {"success": False, "message": "Invalid request"})
                return

        send_response(client_socket, response)

    except (json.JSONDecodeError, UnicodeDecodeError):
        send_response(client_socket, {"success": False, "message": "Invalid JSON request"})
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
