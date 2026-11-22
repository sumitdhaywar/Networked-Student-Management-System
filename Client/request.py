import socket
import json

HOST = "127.0.0.1"
PORT = 5000

session_token = None


def send_request(request, data=None):
    global session_token

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.settimeout(10)
        client.connect((HOST, PORT))

        message = {"request": request, "data": data or {}}
        if request != "Login" and session_token:
            message["session_token"] = session_token

        client.sendall(json.dumps(message).encode())
        response = json.loads(client.recv(4096).decode())

        if request == "Login" and response.get("success"):
            session_token = response.get("session_token")

        if request == "Logout" and response.get("success"):
            session_token = None

        return response
    except Exception as e:
        return {"success": False, "message": f"Connection error: {e}"}
    finally:
        client.close()

