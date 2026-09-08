from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route("/payments/charge", methods=["POST"])
def charge_payment():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "status": "failed",
            "message": "Invalid payment request"
        }), 400

    amount = data.get("amount", 0)

    # Simulate payment failure for testing.
    if amount >= 10000:
        return jsonify({
            "status": "failed",
            "message": "Payment service temporarily unavailable"
        }), 500

    if amount >= 5000:
        return jsonify({
            "status": "failed",
            "message": "Payment request rejected"
        }), 400

    # Normal successful payment.
    return jsonify({
        "transactionId": "TXN-1001",
        "status": "SUCCESS",
        "message": "Payment successful"
    }), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)