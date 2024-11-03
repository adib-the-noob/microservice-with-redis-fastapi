from pydantic import BaseModel
from enum import Enum as PyEnum

class OrderStatus(PyEnum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"


class Order(BaseModel):
    product_id: str
    price: float
    fee: float
    total: float
    status: OrderStatus = OrderStatus.pending
    
    class Config:
        from_attributes = True
        
    
class CreateOrder(BaseModel):
    product_id: str
    amount: int