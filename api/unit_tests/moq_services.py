class AlwaysDenyPaymentService:
    def pay(self, payment_data):
        return False

class AlwaysAllowPaymentService:
    def pay(self, payment_data):
        return True