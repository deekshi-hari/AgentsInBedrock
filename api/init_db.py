import asyncio

from sqlalchemy import text

from api.database import Base, engine
from api.models import ProductInfo


async def init_db():
    async with engine.begin() as conn:
        await conn.execute(text('CREATE SCHEMA IF NOT EXISTS "TechProducts"'))
        await conn.run_sync(Base.metadata.create_all, tables=[ProductInfo.__table__], checkfirst=True)
    print("Database initialized: schema 'TechProducts' and table 'product_info' are ready.")


if __name__ == "__main__":
    asyncio.run(init_db())
