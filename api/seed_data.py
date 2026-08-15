import asyncio

from sqlalchemy.dialects.postgresql import insert

from api.database import async_session
from api.models import ProductInfo
from datas.products import PRODUCTS


async def seed():
    async with async_session() as session:
        for name, info in PRODUCTS.items():
            stmt = insert(ProductInfo).values(
                name=name,
                description=info["description"],
                price=info["price"],
                rating=info["rating"],
                reviews=int(info["rating"] * 20),
            ).on_conflict_do_nothing(index_elements=["name"])
            await session.execute(stmt)
        await session.commit()
    print(f"Seeded {len(PRODUCTS)} products (existing ones skipped).")


if __name__ == "__main__":
    asyncio.run(seed())
