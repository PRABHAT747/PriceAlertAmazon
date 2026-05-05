from db.database import SessionLocal
from db.models import User, Product, Subscription
from utils.validations.url_validations.url_utils import is_valid_amazon_url, normalize_amazon_url
from services.email_service.notifier import send_email

def create_subscription(email, url, target_price, name = None):
    db = SessionLocal()
    try:
        if not is_valid_amazon_url(url):
            send_email(
                email,
                "Invalid Amazon URL",
                "Please provide a valid Amazon URL in this format: https://www.amazon.in/dp/XXXXXXXXXX"
            )
            return {"error": "Invalid URL"}
        url = normalize_amazon_url(url)

        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(email=email)
            db.add(user)
            db.commit()
        product = db.query(Product).filter(Product.url == url).first()

        if not product:
            product = Product(url=url, name=name)
            db.add(product)
            db.commit()
        else:
            if not product.name and name:
                product.name = name


        existing = db.query(Subscription).filter(
            Subscription.user_id == user.id,
            Subscription.product_id == product.id
        ).first()

        if existing:
            existing.target_price = target_price
        else:
            sub = Subscription(
                user_id=user.id,
                product_id=product.id,
                target_price=target_price
            )
            db.add(sub)
        db.commit()
        return {"message": "Subscription saved - You will be notified if the price goes down"}

    finally:
        db.close()

def delete_subscription(email, url):
    db = SessionLocal()

    try:
        url = normalize_amazon_url(url)

        user = db.query(User).filter(User.email == email).first()
        if not user:
            return {"error": "User not found"}

        product = db.query(Product).filter(Product.url == url).first()
        if not product:
            return {"error": "Product not found"}

        sub = db.query(Subscription).filter(
            Subscription.user_id == user.id,
            Subscription.product_id == product.id
        ).first()

        if not sub:
            return {"error": "Subscription not found"}

        db.delete(sub)
        db.commit()

        return {"message": "Subscription removed"}

    finally:
        db.close()