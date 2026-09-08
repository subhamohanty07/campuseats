from dataclasses import dataclass, field
from typing import List


VALID_STATUSES = {
    "PLACED",
    "CONFIRMED",
    "PREPARING",
    "READY",
    "OUT_FOR_DELIVERY",
    "DELIVERED",
    "CANCELLED",
}


@dataclass
class OrderItem:
    item_id: str
    quantity: int
    price: float


@dataclass
class Order:
    order_id: str
    student_id: str
    address_id: str
    items: List[OrderItem] = field(default_factory=list)
    total: float = 0.0
    status: str = "PLACED"

    def as_json(self):
        return {
            "orderId": self.order_id,
            "studentId": self.student_id,
            "addressId": self.address_id,
            "items": [
                {
                    "itemId": item.item_id,
                    "quantity": item.quantity,
                    "price": item.price,
                }
                for item in self.items
            ],
            "total": self.total,
            "status": self.status,
        }