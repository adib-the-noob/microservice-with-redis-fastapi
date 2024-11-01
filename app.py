from fastapi import FastAPI
from pydantic import BaseModel
from redis_om import get_redis_connection, HashModel

app = FastAPI()

redis = get_redis_connection(
    host="localhost",
    port=6379,
    db=0,   
    decode_responses=True
)

class Product(HashModel):
    name: str
    price: float
    quantity: int
    
    class Meta:
        database = redis
    
class ProductRq(BaseModel):
    name: str
    price: float
    quantity: int
        
    
@app.get(
    "/products",
)
async def get_products():
    products = Product.all_pks()
    return products

@app.post(
    path="/create_product",
)
async def create_product(product: ProductRq):
    product = Product(**product.model_dump())
    return product.save()