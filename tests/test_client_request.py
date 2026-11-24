import json
from unittest.mock import patch

from Client import request as client_request


class ChunkedResponseSocket:
    def __init__(self, chunks):
        self.chunks = list(chunks)
        self.sent = b""

    def settimeout(self, timeout):
        pass

    def connect(self, address):
        pass

    def sendall(self, data):
        self.sent = data

    def recv(self, size):
        if not self.chunks:
            return b""
        chunk = self.chunks.pop(0)
        self.chunks[:0] = [chunk[size:]] if len(chunk) > size else []
        return chunk[:size]

    def close(self):
        pass


def test_send_request_reads_full_large_response():
    expected = {"success": True, "data": "x" * 10000}
    encoded = json.dumps(expected).encode("utf-8")
    client = ChunkedResponseSocket((encoded[:4096], encoded[4096:]))

    with patch.object(client_request.socket, "socket", return_value=client):
        response = client_request.send_request("Test")

    assert response == expected
