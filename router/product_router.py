from fastapi import APIRouter
from redis_models.product import ProductModel
from schemas.products import Product

router = APIRouter(
    prefix="/product",
    tags=["product"],
)    

@router.get("/all-products")
async def get_products():
    products = ProductModel.all_pks()
    return products

@router.post("/add-product", response_model=None)
async def create_product(product: Product):
    product = ProductModel(
        name=product.name,
        price=product.price,
        quantity=product.quantity
    )
    product.save()
    return product