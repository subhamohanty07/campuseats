import logging

from flask import Flask, jsonify, request, make_response
from models import Order, OrderItem, VALID_STATUSES
from store import OrderStore
from errors import problem, OrderError
from payment_client import charge_payment


app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

store = OrderStore()


def validate(data):
    """
    Validate the complete request body before accessing
    individual body fields.
    """

    if not isinstance(data, dict):
        raise OrderError(
            400,
            "Malformed request body",
            "Request body must be a JSON object."
        )

    required_fields = ["studentId", "addressId", "items"]

    for field in required_fields:
        if field not in data:
            raise OrderError(
                400,
                "Malformed request body",
                f"Missing required field: {field}."
            )

    if not isinstance(data["items"], list) or len(data["items"]) == 0:
        raise OrderError(
            422,
            "Invalid order",
            "Order must contain at least one item."
        )

    for item in data["items"]:

        if not isinstance(item, dict):
            raise OrderError(
                400,
                "Malformed request body",
                "Each order item must be an object."
            )

        if "itemId" not in item or "quantity" not in item:
            raise OrderError(
                400,
                "Malformed request body",
                "Each item requires itemId and quantity."
            )

        if (
            not isinstance(item["quantity"], int)
            or item["quantity"] < 1
        ):
            raise OrderError(
                422,
                "Invalid order",
                "Item quantity must be at least 1."
            )


@app.errorhandler(OrderError)
def handle_order_error(error):

    return jsonify(
        problem(
            error.status,
            error.title,
            error.detail
        )
    ), error.status


@app.route("/orders", methods=["POST"])
def create_order():

    idempotency_key = request.headers.get("Idempotency-Key")

    if not idempotency_key:

        return jsonify(
            problem(
                400,
                "Missing Idempotency-Key",
                "Idempotency-Key header is required."
            )
        ), 400

    data = request.get_json(silent=True)

    if data is None:

        return jsonify(
            problem(
                400,
                "Malformed request body",
                "Request body must contain valid JSON."
            )
        ), 400

    # Validate the complete request before using body fields.
    validate(data)

    # Check whether this request was already processed.
    existing = store.get_idempotency_record(idempotency_key)

    if existing:

        # Same key with different request = conflict.
        if existing["request"] != data:

            return jsonify(
                problem(
                    409,
                    "Idempotency key conflict",
                    "The same Idempotency-Key was already used "
                    "with a different request."
                )
            ), 409

        # Return the original result without creating another order.
        saved_response = existing["response"]

        response = make_response(
            jsonify(saved_response["body"]),
            saved_response["status"]
        )

        if saved_response.get("location"):
            response.headers["Location"] = saved_response["location"]

        return response

    # Build order items.
    items = []

    for item in data["items"]:

        # Fixed catalogue price for this assignment.
        price = 249.50

        items.append(
            OrderItem(
                item_id=item["itemId"],
                quantity=item["quantity"],
                price=price
            )
        )

    # Calculate order total.
    total = sum(
        item.price * item.quantity
        for item in items
    )

    # Generate the order ID before calling Payments.
    order_id = store.generate_order_id()

    # Call Payments Service.
    payment_result = charge_payment(
        order_id,
        total,
        idempotency_key
    )

    # Payment service explicitly rejected the request.
    if (
        not payment_result["success"]
        and not payment_result["fallback"]
    ):

        return jsonify(
            problem(
                422,
                "Payment declined",
                payment_result["reason"]
            )
        ), 422

    # Payment service could not be reached successfully.
    if payment_result["fallback"]:

        return jsonify(
            problem(
                503,
                "Payment service unavailable",
                "The payment service could not be reached "
                "after retries. The order was not created. "
                "Please try again later."
            )
        ), 503

    # Create the order only after successful payment.
    order = Order(
        order_id=order_id,
        student_id=data["studentId"],
        address_id=data["addressId"],
        items=items,
        total=total,
        status="PLACED"
    )

    store.save(order)

    # Published representation.
    response_body = order.as_json()

    location = f"/orders/{order_id}"

    # Store the idempotency key and original result.
    store.save_idempotency_record(
        idempotency_key,
        data,
        {
            "body": response_body,
            "status": 201,
            "location": location
        }
    )

    response = make_response(
        jsonify(response_body),
        201
    )

    response.headers["Location"] = location

    return response


@app.route("/orders/<order_id>", methods=["GET"])
def get_order(order_id):

    order = store.get(order_id)

    if order is None:

        return jsonify(
            problem(
                404,
                "Order not found",
                f"No order exists with id {order_id}."
            )
        ), 404

    return jsonify(order.as_json()), 200


@app.route("/orders", methods=["GET"])
def list_orders():

    status = request.args.get("status")

    if status and status not in VALID_STATUSES:

        return jsonify(
            problem(
                400,
                "Invalid status filter",
                f"'{status}' is not a valid order status."
            )
        ), 400

    orders = store.list_orders(status)

    return jsonify(
        [order.as_json() for order in orders]
    ), 200


@app.route("/orders/<order_id>/cancellation", methods=["POST"])
def cancel_order(order_id):

    order = store.get(order_id)

    if order is None:

        return jsonify(
            problem(
                404,
                "Order not found",
                f"No order exists with id {order_id}."
            )
        ), 404

    if order.status in {"DELIVERED", "CANCELLED"}:

        return jsonify(
            problem(
                409,
                "Order cannot be cancelled",
                f"Order {order_id} cannot be cancelled "
                f"from status {order.status}."
            )
        ), 409

    order.status = "CANCELLED"

    return jsonify(order.as_json()), 200


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )