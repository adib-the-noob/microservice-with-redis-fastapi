from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated

from schemas.products import Product
from redis_models.product import ProductModel


router = APIRouter(
    prefix="/product",
    tags=["product"],
)    


@router.get("/all-products")
async def get_products():
    products = ProductModel.all_pks()
    
    # load all datas 
    datas = [ProductModel.get(product) for product in products]
    return datas


@router.post("/add-product", response_model=None)
async def create_product(product: Product):
    product = ProductModel(
        name=product.name,
        price=product.price,
        quantity=product.quantity
    )
    product.save()
    return product


@router.get("/get-product/{product_id}")
async def get_product(product_id: str):
    product = ProductModel.get(product_id)
    return product


@router.patch("/update-product/{product_id}", response_model=None)
async def update_product(product_id: str, updated_data: Product = Depends()):
    product = ProductModel.get(product_id)
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product.name = updated_data.name if updated_data.name else product.name
    product.price = updated_data.price if updated_data.price else product.price
    product.quantity = updated_data.quantity if updated_data.quantity else product.quantity
    
    product.save()
    
    return product