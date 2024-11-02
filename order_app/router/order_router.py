from fastapi import APIRouter, HTTPException, Depends
from redis_models.orders import OrderModel
from schemas.orders import Order, OrderStatus
import requests

from starlette.requests import Request


router = APIRouter(
    prefix="/order",
    tags=["order"],
)

@router.get("/all-orders")
async def get_all_orders():
    pass

@router.post("/add-order", response_model=None)
async def create_order(request: Request):
    
    body = await request.json() # get the id and quantity of the product
    
    try:
        product_id = body[0]['product_id']
        print(product_id)
        
        req = requests.get("http://127.0.0.1:8000/product/get-product/%s" % product_id)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    product = req.json()
    print(product)
    
    price = product['price']
    quantity = product['quantity']
    
    total_price = price * quantity
    
    order = OrderModel(
        product_id=product_id,
        price=price,
        fee=5,
        total=total_price
    )
    order.save()
    return order