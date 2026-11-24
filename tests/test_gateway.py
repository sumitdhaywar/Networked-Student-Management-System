import json
import socketserver
import threading
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from unittest.mock import patch

from frontend import gateway


SERVER_COMMANDS = {
    "Add_Student",
    "Search_Student",
    "Display All Student",
    "update_student",
    "Delete_Student",
    "Add_Marks",
    "calculate_result",
    "display_topper",
    "Display All Result",
    "Update_Marks",
    "Delete_Marks",
    "result_statistics",
    "course_toppers",
    "Add_Teacher",
    "Search_Teacher",
    "Display All Teachers",
    "Update_Teacher",
    "Delete_Teacher",
    "Add_Course",
    "Search_Course",
    "Display All Courses",
    "Update_Course",
    "Delete_Course",
    "Allocate_Student",
    "Display All Allocations",
    "Remove_Allocation",
    "View_My_Allocated_Students",
    "Enroll_Student",
    "Display All Enrollments",
    "Remove_Enrollment",
    "Set_Student_Credentials",
}


def _post_json(url, payload):
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        response = urlopen(request, timeout=3)
    except HTTPError as error:
        response = error
    with response:
        return response.status, json.loads(response.read().decode("utf-8"))


def test_gateway_allows_every_server_command():
    assert gateway.ALLOWED_COMMANDS == SERVER_COMMANDS


def test_gateway_rejects_non_object_request_data():
    server = ThreadingHTTPServer(("127.0.0.1", 0), gateway.GatewayHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_address[1]}/api/command"
    try:
        with patch.object(gateway, "tcp_request") as tcp_request:
            for payload in (
                [],
                {"request": [], "data": {}},
                {"request": "Search_Student", "data": []},
            ):
                status, response = _post_json(base_url, payload)
                assert status == 400
                assert response["success"] is False
            tcp_request.assert_not_called()
    finally:
        server.shutdown()
        thread.join()
        server.server_close()


def test_gateway_forwards_whitelisted_command():
    server = ThreadingHTTPServer(("127.0.0.1", 0), gateway.GatewayHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_address[1]}/api/command"
    try:
        with patch.object(
            gateway, "tcp_request", return_value={"success": True, "data": []}
        ) as tcp_request:
            status, response = _post_json(
                base_url,
                {"request": "Display All Teachers", "data": {}},
            )
        assert status == 200
        assert response["success"] is True
        tcp_request.assert_called_once_with(
            "Display All Teachers", {}, session_token=None
        )
    finally:
        server.shutdown()
        thread.join()
        server.server_close()


def test_student_response_sanitizer_removes_legacy_password_hash():
    response = {
        "success": True,
        "data": [(101, "Student", 18, "student101", "salt$hash")],
    }

    sanitized = gateway.sanitize_response("Display All Student", response)

    assert sanitized["data"] == [
        {"id": 101, "name": "Student", "age": 18, "user_name": "student101"}
    ]


def test_http_gateway_round_trips_a_large_tcp_response():
    class TcpHandler(socketserver.BaseRequestHandler):
        def handle(self):
            self.server.received = json.loads(self.request.recv(4096).decode("utf-8"))
            response = json.dumps(
                {"success": True, "data": "x" * 10000}
            ).encode("utf-8")
            self.request.sendall(response)

    tcp_server = socketserver.ThreadingTCPServer(("127.0.0.1", 0), TcpHandler)
    tcp_thread = threading.Thread(target=tcp_server.serve_forever)
    tcp_thread.start()
    http_server = ThreadingHTTPServer(("127.0.0.1", 0), gateway.GatewayHandler)
    http_thread = threading.Thread(target=http_server.serve_forever)
    http_thread.start()

    try:
        with patch.object(gateway, "SERVER_HOST", "127.0.0.1"), patch.object(
            gateway, "SERVER_PORT", tcp_server.server_address[1]
        ):
            status, response = _post_json(
                f"http://127.0.0.1:{http_server.server_address[1]}/api/command",
                {
                    "request": "Search_Student",
                    "data": {"id": 101},
                },
            )

        assert status == 200
        assert response["success"] is True
        assert len(response["data"]) == 10000
        assert tcp_server.received == {
            "request": "Search_Student",
            "data": {"id": 101},
        }
    finally:
        http_server.shutdown()
        http_thread.join()
        http_server.server_close()
        tcp_server.shutdown()
        tcp_thread.join()
        tcp_server.server_close()
