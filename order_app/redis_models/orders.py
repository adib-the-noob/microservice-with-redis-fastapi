from redis_om import HashModel
from schemas.orders import Order
from redis_client_2 import redis_client_2

class OrderModel(Order, HashModel):
    class Meta:
        database = redis_client_2