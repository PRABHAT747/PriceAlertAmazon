from db.database import SessionLocal
from db.models import Product, Subscription, PriceHistory, User
from scraper.amazon_scraper import get_product_details
from utils.Selenium.driver import get_driver
from utils.Alert_Utils.alert_service import should_alert
from services.email_service.notifier import send_email

def run_tracker():
    db = SessionLocal()

    driver = get_driver()

    try:
        products = db.query(Product).all()

        for product in products:
            try:
                price, name= get_product_details(driver, product.url)

                if not product.name:
                    product.name=name

                db.add(PriceHistory(product_id=product.id, price=price))

                subs = db.query(Subscription).filter(
                    Subscription.product_id == product.id
                ).all()

                for sub in subs:
                    user = db.query(User).filter(User.id == sub.user_id).first()

                    if should_alert(sub, price):
                        send_email(
                            user.email,
                            "Price Alert 🚨",
                            f"{product.name}\n\nPrice dropped to: ₹{price}\n Visit link: {product.url}"
                        )
                        sub.last_notified_price = price

                product.last_price = price
                db.commit()

            except Exception as e:
                print("Error scraping:", e)

    finally:
        driver.quit()
        db.close()