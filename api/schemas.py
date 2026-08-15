from datetime import datetime

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    rating: float = 0
    reviews: int = 0


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    rating: float | None = None
    reviews: int | None = None


class ProductRead(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    rating: float
    reviews: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
