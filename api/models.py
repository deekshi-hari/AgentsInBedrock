from sqlalchemy import Column, DateTime, Float, Integer, Numeric, String, Text, func

from api.database import Base


class ProductInfo(Base):
    __tablename__ = "product_info"
    __table_args__ = {"schema": "TechProducts"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    rating = Column(Float, default=0)
    reviews = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
