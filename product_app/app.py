from fastapi import FastAPI
from router import product_router

app = FastAPI(
    title="Redis FastAPI",
    description="FastAPI with Redis",
    version="0.1",
)

app.include_router(product_router.router)
