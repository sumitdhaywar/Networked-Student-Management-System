#!/usr/bin/env python3
"""Translate browser HTTP requests into the NSMS socket protocol.

    Browser -> gateway.py (HTTP) -> server.py (TCP)

Start server.py first, then run this file and open the printed UI address.
The host and port values can be overridden with NSMS_SERVER_HOST,
NSMS_SERVER_PORT, NSMS_GATEWAY_HOST, and NSMS_GATEWAY_PORT.
"""

import json
import os
import socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

SERVER_HOST = os.environ.get("NSMS_SERVER_HOST", "127.0.0.1")
SERVER_PORT = int(os.environ.get("NSMS_SERVER_PORT", "5000"))
GATEWAY_HOST = os.environ.get("NSMS_GATEWAY_HOST", "127.0.0.1")
GATEWAY_PORT = int(os.environ.get("NSMS_GATEWAY_PORT", "8080"))

ROOT = os.path.dirname(os.path.abspath(__file__))

# Keep this allowlist aligned with the requests routed in server.py.
ALLOWED_COMMANDS = {
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

CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".mjs": "text/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".ico": "image/x-icon",
    ".webp": "image/webp",
    ".woff": "font/woff",
    ".woff2": "font/woff2",
    ".map": "application/json; charset=utf-8",
}


def tcp_request(request, data=None, session_token=None):
    """Send one JSON request to server.py and return the decoded response.

    The server accepts a complete JSON object followed by socket shutdown,
    which is how this gateway frames each request.
    """
    payload = {"request": request, "data": data or {}}
    if session_token:
        payload["session_token"] = session_token

    with socket.create_connection((SERVER_HOST, SERVER_PORT), timeout=10) as sock:
        sock.sendall(json.dumps(payload).encode("utf-8"))

        chunks = []
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            chunks.append(chunk)

    if not chunks:
        return {"success": False, "message": "Empty response from the NSMS server"}

    return json.loads(b"".join(chunks).decode("utf-8"))


def _student_object(row):
    """Turn the server's student tuple into a clean object (no password hash)."""
    if isinstance(row, dict):
        return {
            key: value
            for key, value in row.items()
            if "password" not in key.lower() and "hash" not in key.lower()
        }

    if isinstance(row, (list, tuple)):
        keys = ["id", "name", "age", "user_name", "password_hash"]
        obj = {}
        for index, value in enumerate(row):
            key = keys[index] if index < len(keys) else f"field_{index}"
            obj[key] = value
        obj.pop("password_hash", None)
        return obj

    return row


def _topper_object(row):
    """Topper query returns (id, name, sum_marks, average_marks)."""
    if isinstance(row, dict):
        return row
    if isinstance(row, (list, tuple)):
        keys = ["id", "name", "total", "average"]
        return {
            (keys[index] if index < len(keys) else f"field_{index}"): value
            for index, value in enumerate(row)
        }
    return row


def sanitize_response(request, response):
    """Replace response data in place with browser-safe objects."""
    if not isinstance(response, dict):
        return response

    if request == "Search_Student" and response.get("success"):
        response["data"] = _student_object(response.get("data"))
    elif request == "Display All Student" and response.get("success"):
        response["data"] = [_student_object(row) for row in (response.get("data") or [])]
    elif request == "display_topper" and response.get("success"):
        response["data"] = _topper_object(response.get("data"))

    return response


def health_payload():
    """Report gateway success even when the TCP server is unreachable."""
    reachable = False
    error = None
    try:
        with socket.create_connection((SERVER_HOST, SERVER_PORT), timeout=2):
            reachable = True
    except OSError as exc:
        error = str(exc)

    payload = {
        "success": True,
        "server": {
            "host": SERVER_HOST,
            "port": SERVER_PORT,
            "reachable": reachable,
        },
    }
    if error:
        payload["server"]["error"] = error
    return payload


class GatewayHandler(BaseHTTPRequestHandler):
    server_version = "NSMSGateway/1.0"

    def log_message(self, fmt, *args):
        print("[gateway] " + (fmt % args))

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Session-Token")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")

    def _send_json(self, payload, status=200):
        body = json.dumps(payload, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            raise ValueError("Invalid Content-Length")
        if length <= 0:
            return {}
        if length > 1024 * 1024:
            raise ValueError("Request body is too large")
        raw = self.rfile.read(length)
        if not raw:
            return {}
        body = json.loads(raw.decode("utf-8"))
        if not isinstance(body, dict):
            raise ValueError("JSON request body must be an object")
        return body

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/health":
            self._send_json(health_payload())
            return
        self._serve_static(path)

    def do_POST(self):
        path = urlparse(self.path).path

        try:
            body = self._read_json_body()
        except ValueError:
            self._send_json({"success": False, "message": "Invalid JSON body"}, status=400)
            return

        token = self.headers.get("X-Session-Token")

        try:
            if path == "/api/login":
                response = tcp_request(
                    "Login",
                    {
                        "username": body.get("username", ""),
                        "password": body.get("password", ""),
                    },
                )
            elif path == "/api/logout":
                response = tcp_request("Logout", session_token=token)
            elif path == "/api/command":
                command = body.get("request")
                data = body.get("data", {})
                if not isinstance(command, str) or command not in ALLOWED_COMMANDS:
                    self._send_json(
                        {"success": False, "message": "Unsupported request"}, status=400
                    )
                    return
                if not isinstance(data, dict):
                    self._send_json(
                        {"success": False, "message": "Request data must be an object"},
                        status=400,
                    )
                    return
                response = tcp_request(
                    command, data, session_token=token
                )
                response = sanitize_response(command, response)
            else:
                self._send_json({"success": False, "message": "Not found"}, status=404)
                return
        except (ConnectionError, socket.timeout, OSError) as exc:
            self._send_json(
                {
                    "success": False,
                    "message": (
                        f"Cannot reach the NSMS server at {SERVER_HOST}:{SERVER_PORT}. "
                        f"Make sure server.py is running. ({exc})"
                    ),
                },
                status=502,
            )
            return
        except json.JSONDecodeError:
            self._send_json(
                {"success": False, "message": "The NSMS server returned an invalid response"},
                status=502,
            )
            return

        self._send_json(response)

    def _serve_static(self, path):
        if path in ("", "/"):
            path = "/index.html"

        relative = path.lstrip("/")
        full_path = os.path.abspath(os.path.join(ROOT, relative))

        try:
            inside_root = os.path.commonpath([ROOT, full_path]) == ROOT
        except ValueError:
            inside_root = False

        if not inside_root or not os.path.isfile(full_path):
            self._send_json({"success": False, "message": "Not found"}, status=404)
            return

        extension = os.path.splitext(full_path)[1].lower()
        content_type = CONTENT_TYPES.get(extension, "application/octet-stream")

        with open(full_path, "rb") as handle:
            data = handle.read()

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self._cors()
        self.end_headers()
        self.wfile.write(data)


def main():
    server = ThreadingHTTPServer((GATEWAY_HOST, GATEWAY_PORT), GatewayHandler)
    print("NSMS frontend gateway running")
    print(f"  UI      : http://{GATEWAY_HOST}:{GATEWAY_PORT}")
    print(f"  Server  : tcp://{SERVER_HOST}:{SERVER_PORT}")
    print("  Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nGateway stopped")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
