class RefundCase:
    """Simple workflow class for state-based testing demos."""

    def __init__(self, priority="normal"):
        allowed_priorities = {"normal", "vip"}
        if priority not in allowed_priorities:
            raise ValueError("priority must be normal or vip")

        self.priority = priority
        self.state = "draft"
        self.refund_amount = 0

    def submit(self):
        if self.state != "draft":
            return "already_submitted"

        self.state = "submitted"
        return "submitted"

    def flag_for_review(self):
        if self.state == "draft":
            raise ValueError("case must be submitted before review")

        if self.state in {"approved", "rejected", "closed"}:
            return "immutable"

        self.state = "under_review"
        return "under_review"

    def approve(self, refund_amount):
        if refund_amount <= 0:
            raise ValueError("refund_amount must be positive")

        if self.state not in {"submitted", "under_review"}:
            raise ValueError("case is not ready for approval")

        self.refund_amount = refund_amount
        self.state = "approved"

        if self.priority == "vip" and refund_amount >= 200:
            return "approved_fast_track"

        return "approved"

    def reject(self, reason):
        if not reason:
            raise ValueError("reason is required")

        if self.state not in {"submitted", "under_review"}:
            raise ValueError("case is not ready for rejection")

        self.state = "rejected"
        return "rejected"

    def close(self):
        if self.state == "closed":
            return "already_closed"

        if self.state not in {"approved", "rejected"}:
            raise ValueError("case must be resolved before closing")

        self.state = "closed"
        return "closed"
