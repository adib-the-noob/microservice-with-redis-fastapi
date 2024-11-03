from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse

from redis_models.orders import OrderModel
from schemas.orders import Order, OrderStatus
import requests

from starlette.requests import Request
import time


router = APIRouter(
    prefix="/order",
    tags=["order"],
)

@router.get("/all-orders")
async def get_all_orders():
    pass

@router.post("/add-order", response_model=None)
async def create_order(request: Request):
    try:    
        body = await request.json() # get the id and quantity of the product 
        
        try:
            product_id = body[0]['product_id']
            print(product_id)
            
            req = requests.get("http://127.0.0.1:8000/product/get-product/%s" % product_id)
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=404, detail=str(e))
        
        product = req.json()

        price = product['price']
        quantity = product['quantity']
        name = product['name']
        
        fee = float(price) * 0.2
        total = float(price) + fee * int(quantity)


        order = OrderModel(
            product_id=product_id,
            price=price,
            fee=fee,
            total=total,
            status=OrderStatus.pending
        )
        order.save()
        
        change_order_status(order=order, status=OrderStatus.completed)
        
        return JSONResponse({
            "status": "success",
            "data": {
                "product_id": product_id,
                "name": name,
                "price": price,
                "quantity": quantity,
                "fee": 0.2 * price,
                "total": price + 0.2 * price,
                "order_status": order.status.value
            }
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
def change_order_status(order: OrderModel, status: OrderStatus):
    time.sleep(5)
    order.status = status
    order.save()
    return order