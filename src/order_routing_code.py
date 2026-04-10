def route_order(order_total, customer_tier, is_express, has_coupon, destination):
    """Classify how an order should be handled.

    Rules:
    - ``order_total`` must be zero or greater.
    - ``customer_tier`` must be one of: ``standard``, ``silver``, ``gold``.
    - ``destination`` must be either ``domestic`` or ``international``.
    - International express shipping requires an order total of at least 50.
    - VIP processing applies to gold customers, or to silver customers with orders of 150 or more.
    - Free shipping applies only to domestic orders when the total is at least 100,
      or when the customer tier is gold.
    - Coupon discounts apply only when ``has_coupon`` is true and the total is at least 80.

    Return values:
    - ``vip_free_shipping_discount``: VIP order with free shipping and a valid coupon.
    - ``vip_free_shipping``: VIP order with free shipping but no valid coupon.
    - ``international_express``: valid international express order.
    - ``discount_only``: coupon discount applies, but the order is not VIP with free shipping.
    - ``manual_review``: small domestic order under 20 without other special handling.
    - ``standard``: none of the special cases apply.
    """
    allowed_tiers = {"standard", "silver", "gold"}
    allowed_destinations = {"domestic", "international"}

    if order_total < 0:
        raise ValueError("order_total must be non-negative")

    if customer_tier not in allowed_tiers:
        raise ValueError("customer_tier must be standard, silver, or gold")

    if destination not in allowed_destinations:
        raise ValueError("destination must be domestic or international")

    if destination == "international" and is_express and order_total < 50:
        raise ValueError("international express requires order_total >= 50")

    vip_processing = customer_tier == "gold" or (
        customer_tier == "silver" and order_total >= 150
    )
    free_shipping = destination == "domestic" and (
        order_total >= 100 or customer_tier == "gold"
    )
    discount_applies = has_coupon and order_total >= 80

    if vip_processing and free_shipping and discount_applies:
        return "vip_free_shipping_discount"

    if vip_processing and free_shipping:
        return "vip_free_shipping"

    if is_express and destination == "international":
        return "international_express"

    if discount_applies:
        return "discount_only"

    if destination == "domestic" and order_total < 20:
        return "manual_review"

    return "standard"
