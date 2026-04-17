"""Example function target used to demo and validate the test generator."""

def assess_refund_request(
    order_total,
    days_since_purchase,
    customer_tier,
    item_condition,
    has_receipt,
    payment_risk_flag,
):
    """Decide how a retail refund request should be handled.

    Inputs:
    - ``order_total``: order value, must be non-negative.
    - ``days_since_purchase``: number of days since purchase, must be non-negative.
    - ``customer_tier``: one of ``standard``, ``silver``, ``gold``.
    - ``item_condition``: one of ``unopened``, ``opened``, ``damaged``.
    - ``has_receipt``: whether the customer has proof of purchase.
    - ``payment_risk_flag``: whether the payment has been flagged for risk.

    Outcomes:
    - ``manual_investigation``: risk-flagged request from a non-gold customer.
    - ``rejected_window``: request outside the allowed time window.
    - ``manual_review``: high-value request without a receipt.
    - ``replacement``: damaged item reported within 30 days.
    - ``full_refund``: unopened item returned within 14 days.
    - ``store_credit``: opened item from a gold customer within 30 days.
    - ``partial_refund``: opened item returned within 14 days.
    - ``rejected_policy``: none of the refund policies apply.
    """
    allowed_tiers = {"standard", "silver", "gold"}
    allowed_conditions = {"unopened", "opened", "damaged"}

    if order_total < 0:
        raise ValueError("order_total must be non-negative")

    if days_since_purchase < 0:
        raise ValueError("days_since_purchase must be non-negative")

    if customer_tier not in allowed_tiers:
        raise ValueError("customer_tier must be standard, silver, or gold")

    if item_condition not in allowed_conditions:
        raise ValueError("item_condition must be unopened, opened, or damaged")

    if payment_risk_flag and customer_tier != "gold":
        return "manual_investigation"

    if days_since_purchase > 60 and customer_tier != "gold":
        return "rejected_window"

    if not has_receipt and order_total > 100:
        return "manual_review"

    if item_condition == "damaged" and days_since_purchase <= 30:
        return "replacement"

    if item_condition == "unopened" and days_since_purchase <= 14:
        return "full_refund"

    if item_condition == "opened" and customer_tier == "gold" and days_since_purchase <= 30:
        return "store_credit"

    if item_condition == "opened" and days_since_purchase <= 14:
        return "partial_refund"

    return "rejected_policy"
