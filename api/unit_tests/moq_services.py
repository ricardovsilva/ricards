from ..exceptions import InsuficientFundsException

class AlwaysDenyPaymentService:
    def pay(self, payment_data):
        raise InsuficientFundsException()

class AlwaysAllowPaymentService:
    def pay(self, payment_data):
        pass