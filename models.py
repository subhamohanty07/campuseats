from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


@dataclass
class Order:
    customer_id: str
    items: list
    delivery_address: str
    idempotency_key: str
    order_id: str = field(default_factory=lambda: "ord-" + uuid4().hex[:12])
    status: str = "PAYMENT_PENDING"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    payment_reference: str | None = None

    def as_json(self):
        return {
            "id": self.order_id,
            "customerId": self.customer_id,
            "items": self.items,
            "deliveryAddress": self.delivery_address,
            "status": self.status,
            "createdAt": self.created_at,
        }
