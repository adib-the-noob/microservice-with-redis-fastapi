from redis_om import HashModel
from redis_client import redis_client

class ProductModel(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis_client