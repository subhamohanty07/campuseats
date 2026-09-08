from models import Order


class OrderStore:
    def __init__(self):
        self.orders = {}
        self.idempotency_records = {}
        self.next_id = 1001

    def generate_order_id(self):
        order_id = f"ORD-{self.next_id}"
        self.next_id += 1
        return order_id

    def save(self, order: Order):
        self.orders[order.order_id] = order

    def get(self, order_id: str):
        return self.orders.get(order_id)

    def list_orders(self, status=None):
        if status:
            return [
                order
                for order in self.orders.values()
                if order.status == status
            ]

        return list(self.orders.values())

    def get_idempotency_record(self, key):
        return self.idempotency_records.get(key)

    def save_idempotency_record(self, key, request_body, response):
        self.idempotency_records[key] = {
            "request": request_body,
            "response": response,
        }