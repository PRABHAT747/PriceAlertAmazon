from fastapi import APIRouter, Query
from services.subscription_service.subscription_service import create_subscription , delete_subscription

router = APIRouter()

@router.post("/subscribe")
def subscribe(
    email: str = Query(..., alias="your_email", description="Enter your email"),
    url: str = Query(..., alias="product_url", description="Enter the amazon product link"),
    target_price: float = Query(... , description="Enter the target price"),
    name: str = Query(None, alias="product_name", description= "Enter the product name")
):
    return create_subscription(email, url, target_price, name)

@router.delete("/unsubscribe")
def unsubscribe(
    email: str = Query(..., alias="your_email", description="Your email"),
    url: str = Query(..., alias="product_url", description="Amazon product URL")
):
    return delete_subscription(email, url)