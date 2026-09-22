from threading import RLock


class OrderStore:
    """In-memory order store with an atomic idempotency-key index."""

    def __init__(self):
        self._orders = {}
        self._keys = {}
        self._lock = RLock()

    def create_once(self, order):
        with self._lock:
            existing = self._keys.get(order.idempotency_key)
            if existing is not None:
                return self._orders[existing], False
            self._orders[order.order_id] = order
            self._keys[order.idempotency_key] = order.order_id
            return order, True

    def get(self, order_id):
        return self._orders.get(order_id)

    def list(self, status=None):
        rows = list(self._orders.values())
        return rows if status is None else [row for row in rows if row.status == status]

    def delete(self, order_id):
        with self._lock:
            order = self._orders.pop(order_id, None)
            if order is not None:
                self._keys.pop(order.idempotency_key, None)
