from ..models import Account
from ..models import Transaction

class PaymentService:
    def pay(self, transaction_data):
        AUTHORISATION, PRESENTMENT = 'A', 'P'
        transaction = Transaction.from_json(transaction_data)

        if transaction.type == AUTHORISATION:
            return self._authorize(transaction)
        elif transaction.type == PRESENTMENT:
            return self._execute_presentment(transaction)
        else:
            raise Exception(transaction.type + " transaction type was not implemented yet!")

    def _authorize(self, transaction):
        account = Account.objects.find(card_id=transaction.card_id).first


    def _execute_presentment(self, transaction):
        pass