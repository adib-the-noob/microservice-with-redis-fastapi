from pydantic import BaseModel, Field
from typing import Optional

class Product(BaseModel):
    name: Optional[str] = Field(None, title="Product Name")
    price: Optional[float] = Field(None, title="Product Price")
    quantity: Optional[int] = Field(None, title="Product Quantity")
    
    class Config:
        from_attributes = True
        
class ProductInDB(Product):
    pk: str
    class Config:
        from_attributes = True
        
