from fastapi import APIRouter
from db.database import SessionLocal
from db.models import Product, PriceHistory

router = APIRouter()

@router.get("/history")
def history(url: str):
    db = SessionLocal()

    try:
        product = db.query(Product).filter(Product.url == url).first()

        if not product:
            return []

        data = db.query(PriceHistory).filter(
            PriceHistory.product_id == product.id
        ).all()

        return [{"price": p.price, "time": p.created_at} for p in data]

    finally:
        db.close()