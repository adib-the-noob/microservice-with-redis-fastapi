from pydantic import BaseModel
from enum import Enum as PyEnum

class OrderStatus(PyEnum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"


class Order(BaseModel):
    product_id: str
    price: int
    fee: int 
    total: int
    status: OrderStatus = OrderStatus.pending
    
    class Config:
        from_attributes = True