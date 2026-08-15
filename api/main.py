from fastapi import FastAPI

from api.routers import products

app = FastAPI(title="TechProducts API")
app.include_router(products.router)
