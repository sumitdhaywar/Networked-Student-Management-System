from contextlib import contextmanager
import importlib
import sys
import types
from unittest.mock import patch

import pytest


@contextmanager
def _load_server_with_stubbed_dependencies():
    services = types.ModuleType("services")
    services.__path__ = []
    service_names = (
        "student_services",
        "auth_services",
        "result_services",
        "teacher_services",
        "course_services",
        "allocation_services",
        "enrollment_services",
    )
    modules = {"services": services}
    for name in service_names:
        module_name = f"services.{name}"
        module = types.ModuleType(module_name)
        setattr(services, name, module)
        modules[module_name] = module

    database = types.ModuleType("database")
    database.__path__ = []
    connection = types.ModuleType("database.connection")
    connection.mycon = types.SimpleNamespace(in_transaction=False)
    modules["database"] = database
    modules["database.connection"] = connection

    with patch.dict(sys.modules, modules):
        previous_server = sys.modules.pop("server", None)
        try:
            yield importlib.import_module("server")
        finally:
            sys.modules.pop("server", None)
            if previous_server is not None:
                sys.modules["server"] = previous_server


class ChunkedRequestSocket:
    def __init__(self, chunks):
        self.chunks = list(chunks)

    def recv(self, size):
        if not self.chunks:
            return b""
        chunk = self.chunks.pop(0)
        self.chunks[:0] = [chunk[size:]] if len(chunk) > size else []
        return chunk[:size]


def test_server_reads_split_json_request():
    request = b'{"request":"Search_Student","data":{"id":101}}\n'
    with _load_server_with_stubbed_dependencies() as server:
        received = server.receive_request(
            ChunkedRequestSocket((request[:12], request[12:]))
        )

    assert received == {"request": "Search_Student", "data": {"id": 101}}


def test_server_rejects_boolean_and_fractional_ids():
    with _load_server_with_stubbed_dependencies() as server:
        for value in (True, 1.5):
            with pytest.raises(ValueError):
                server.parse_integer({"id": value}, "id")
