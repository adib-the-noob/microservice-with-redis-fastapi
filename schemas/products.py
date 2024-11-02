from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    quantity: int
    
    class Config:
        from_attributes = True