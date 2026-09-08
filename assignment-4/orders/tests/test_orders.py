import pytest

from app import app, store


@pytest.fixture
def client():
    app.config["TESTING"] = True

    # Reset in-memory data before each test
    store.orders.clear()
    store.idempotency_records.clear()
    store.next_id = 1001

    with app.test_client() as client:
        yield client


def create_order_payload():
    return {
        "studentId": "STU-1001",
        "addressId": "ADDR-101",
        "items": [
            {
                "itemId": "ITEM-101",
                "quantity": 2
            }
        ]
    }


def test_create_order(client, monkeypatch):
    # Mock successful Payments response.
    monkeypatch.setattr(
        "app.charge_payment",
        lambda order_id, amount, idempotency_key: {
            "success": True,
            "fallback": False,
            "transactionId": "TXN-TEST-001",
            "message": "Payment successful"
        }
    )

    response = client.post(
        "/orders",
        json=create_order_payload(),
        headers={"Idempotency-Key": "test-create-001"}
    )

    assert response.status_code == 201
    assert response.json["orderId"] == "ORD-1001"
    assert response.json["status"] == "PLACED"
    assert response.json["total"] == 499.0
    assert response.headers["Location"] == "/orders/ORD-1001"


def test_idempotent_repeat_returns_same_order(client, monkeypatch):
    payment_calls = []

    def fake_payment(order_id, amount, idempotency_key):
        payment_calls.append(order_id)

        return {
            "success": True,
            "fallback": False,
            "transactionId": "TXN-TEST-002",
            "message": "Payment successful"
        }

    monkeypatch.setattr(
        "app.charge_payment",
        fake_payment
    )

    payload = create_order_payload()

    first_response = client.post(
        "/orders",
        json=payload,
        headers={"Idempotency-Key": "same-key"}
    )

    second_response = client.post(
        "/orders",
        json=payload,
        headers={"Idempotency-Key": "same-key"}
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201

    assert first_response.json == second_response.json

    # Payment should only be called once.
    assert len(payment_calls) == 1

    # No duplicate order should exist.
    assert len(store.orders) == 1


def test_idempotency_conflict_returns_409(client, monkeypatch):
    monkeypatch.setattr(
        "app.charge_payment",
        lambda order_id, amount, idempotency_key: {
            "success": True,
            "fallback": False,
            "transactionId": "TXN-TEST-003",
            "message": "Payment successful"
        }
    )

    first_payload = create_order_payload()

    second_payload = {
        "studentId": "STU-9999",
        "addressId": "ADDR-999",
        "items": [
            {
                "itemId": "ITEM-999",
                "quantity": 1
            }
        ]
    }

    first_response = client.post(
        "/orders",
        json=first_payload,
        headers={"Idempotency-Key": "conflict-key"}
    )

    second_response = client.post(
        "/orders",
        json=second_payload,
        headers={"Idempotency-Key": "conflict-key"}
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409

    assert second_response.json["title"] == "Idempotency key conflict"
    assert second_response.json["status"] == 409

    assert len(store.orders) == 1


def test_unknown_order_returns_404(client):
    response = client.get("/orders/ORD-9999")

    assert response.status_code == 404
    assert response.json["title"] == "Order not found"
    assert response.json["status"] == 404


def test_payment_failure_fallback_returns_503(client, monkeypatch):
    monkeypatch.setattr(
        "app.charge_payment",
        lambda order_id, amount, idempotency_key: {
            "success": False,
            "fallback": True,
            "reason": "Payments Service unavailable after retries"
        }
    )

    response = client.post(
        "/orders",
        json=create_order_payload(),
        headers={"Idempotency-Key": "fallback-test"}
    )

    assert response.status_code == 503
    assert response.json["title"] == "Payment service unavailable"
    assert response.json["status"] == 503

    # Order must not be created.
    assert len(store.orders) == 0


def test_invalid_quantity_returns_422(client):
    payload = {
        "studentId": "STU-1001",
        "addressId": "ADDR-101",
        "items": [
            {
                "itemId": "ITEM-101",
                "quantity": 0
            }
        ]
    }

    response = client.post(
        "/orders",
        json=payload,
        headers={"Idempotency-Key": "invalid-quantity"}
    )

    assert response.status_code == 422
    assert response.json["title"] == "Invalid order"
    assert response.json["status"] == 422


def test_invalid_status_filter_returns_400(client):
    response = client.get(
        "/orders?status=INVALID_STATUS"
    )

    assert response.status_code == 400
    assert response.json["title"] == "Invalid status filter"
    assert response.json["status"] == 400