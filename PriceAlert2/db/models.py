from sqlalchemy import Column, Integer, Float, String, ForeignKey, UniqueConstraint, DateTime
from datetime import datetime
from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    url = Column(String, unique=True)
    last_price = Column(Float, nullable=True)


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    target_price = Column(Float)
    last_notified_price = Column(Float, nullable=True)

    __table_args__ = (
        UniqueConstraint("user_id", "product_id", name="unique_user_product"),
    )

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)