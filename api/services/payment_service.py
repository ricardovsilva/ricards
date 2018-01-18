from ..models import Account, Transaction, Transfer
from datetime import datetime
from ..exceptions import AuthorisationNotFoundException, AccountNotFoundException

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
        account, created = Account.objects.get_or_create(card_id=transaction.card_id, defaults={'money': 500, 'card_id': transaction.card_id})
        account.reserve_money(transaction.transaction_amount)
        account.save()
        transaction.save()

    def _execute_presentment(self, presentment):
        account = Account.objects.first()
        if not account: raise AccountNotFoundException()

        authorisation = Transaction.objects.filter(
            transaction_id=presentment.transaction_id,
            type='A',
            created_at__lt=datetime.now(),
            processed=False
        ).first()
        if not authorisation: raise AuthorisationNotFoundException()

        Transfer.create(destination='Issuer', amount=presentment.get_revenue(), currency=presentment.billing_currency).save()
        Transfer.create(destination='Scheme', amount=presentment.settlement_amount, currency=presentment.settlement_currency).save()
        account.execute_presentment(presentment.transaction_amount)
        authorisation.processed = True
        presentment.processed = True
        account.save()
        authorisation.save()
        presentment.save()
