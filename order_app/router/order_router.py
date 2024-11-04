from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks
from fastapi.responses import JSONResponse

from typing import List

from redis_models.orders import OrderModel
from schemas.orders import Order, OrderStatus, CreateOrder
from redis_client_2 import redis_client_2

import requests
import time


router = APIRouter(
    prefix="/order",
    tags=["order"],
)

@router.post("/add-order", response_model=None)
async def create_order(order_info: CreateOrder, background_tasks: BackgroundTasks):
    try:    
        try:
            product_id = order_info.product_id
            req = requests.get("http://127.0.0.1:8000/product/get-product/%s" % product_id)
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=404, detail=str(e))
        
        product = req.json()

        price = product.get('price')
        quantity = product.get('quantity')
        name = product.get('name')
        
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
        
        background_tasks.add_task(
            change_order_status, order, OrderStatus.completed
        )
        
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
    time.sleep(10)
    order.status = status
    order.save()
    redis_client_2.xadd(
        name="order_completed",
        fields={
            "order_id": order.pk,
            "product_id": order.product_id,
            "status": order.status.value
        },
        id="*"
    )

@router.get(
    path="/all-orders",
    response_model=None
)
async def get_all_orders():
    orders = OrderModel.all_pks()
    all_orders = []
    for order in orders:
        order = OrderModel.get(order)
        all_orders.append(order)
    return all_orders
    