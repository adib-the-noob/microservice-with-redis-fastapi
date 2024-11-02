from redis_om import HashModel
from redis_client import redis_client

from schemas.products import Product

class ProductModel(Product, HashModel):
    class Meta:
        database = redis_client