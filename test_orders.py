import gzip
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import app

AUTH = {"Authorization": "Bearer group12-test"}


def call(method, path, payload=None, headers=None, query=""):
    raw = json.dumps(payload).encode() if payload is not None else b""
    environ = {
        "REQUEST_METHOD": method,
        "PATH_INFO": path,
        "QUERY_STRING": query,
        "CONTENT_LENGTH": str(len(raw)),
        "wsgi.input": io.BytesIO(raw),
        "REMOTE_ADDR": "127.0.0.1",
    }
    for key, value in (headers or {}).items():
        environ["HTTP_" + key.upper().replace("-", "_")] = value

    result = {}

    def start(status, response_headers):
        result["status"] = status
        result["headers"] = dict(response_headers)

    body = b"".join(app.application(environ, start))
    if result["headers"].get("Content-Encoding") == "gzip":
        body = gzip.decompress(body)
    result["body"] = json.loads(body) if body else None
    return result


def order_payload():
    return {
        "customerId": "student-12",
        "items": [{"menuItemId": "meal-7", "quantity": 1}],
        "deliveryAddress": "Hostel Block C",
    }


def reset_service():
    app.store.reset()
    app._buckets.clear()


def test_create_and_repeat_are_idempotent():
    reset_service()
    first = call("POST", "/orders", order_payload(), AUTH | {"Idempotency-Key": "orders-test-12"})
    second = call("POST", "/orders", order_payload(), AUTH | {"Idempotency-Key": "orders-test-12"})
    assert first["status"].startswith("201")
    assert second["status"].startswith("201")
    assert first["body"]["id"] == second["body"]["id"]
    assert len(app.store.all()) == 1


def test_conditional_read_returns_not_modified():
    reset_service()
    created = call("POST", "/orders", order_payload(), AUTH | {"Idempotency-Key": "etag-test-12"})
    order_id = created["body"]["id"]
    tag = created["headers"]["ETag"]
    checked = call("GET", f"/orders/{order_id}", headers=AUTH | {"If-None-Match": tag})
    assert checked["status"].startswith("304")


def test_missing_auth_is_rejected():
    reset_service()
    result = call("GET", "/orders")
    assert result["status"].startswith("401")
