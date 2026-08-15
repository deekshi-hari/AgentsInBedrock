from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_db
from api.models import ProductInfo
from api.schemas import ProductCreate, ProductRead, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])


async def get_product_or_404(product_id: int, db: AsyncSession) -> ProductInfo:
    product = await db.get(ProductInfo, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    db_product = ProductInfo(**product.model_dump())
    db.add(db_product)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product already exists")
    await db.refresh(db_product)
    return db_product


@router.get("", response_model=list[ProductRead])
async def list_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProductInfo))
    return result.scalars().all()


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    return await get_product_or_404(product_id, db)


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(product_id: int, product: ProductUpdate, db: AsyncSession = Depends(get_db)):
    db_product = await get_product_or_404(product_id, db)
    for field, value in product.model_dump(exclude_unset=True).items():
        setattr(db_product, field, value)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product name already in use")
    await db.refresh(db_product)
    return db_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    db_product = await get_product_or_404(product_id, db)
    await db.delete(db_product)
    await db.commit()
