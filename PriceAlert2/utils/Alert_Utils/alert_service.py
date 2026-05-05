def should_alert(subscription, price):
    if (
        price <= subscription.target_price and
        (subscription.last_notified_price is None or
         subscription.last_notified_price > subscription.target_price)
    ):
        return True
    return False