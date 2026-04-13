class Turnstile:
    """Small stateful example for state-based testing."""

    def __init__(self):
        self.state = "locked"

    def insert_coin(self):
        if self.state == "alarm":
            return "service_required"

        if self.state == "unlocked":
            return "coin_returned"

        self.state = "unlocked"
        return "unlocked"

    def push(self):
        if self.state == "locked":
            self.state = "alarm"
            return "alarm"

        if self.state == "alarm":
            return "alarm"

        self.state = "locked"
        return "passed"

    def reset_alarm(self):
        if self.state != "alarm":
            return "noop"

        self.state = "locked"
        return "reset"

    def lock_for_maintenance(self):
        if self.state == "unlocked":
            raise ValueError("cannot lock while the turnstile is open")

        self.state = "locked"
        return "locked"
