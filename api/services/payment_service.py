from api.models import Account, Transaction, Transfer
from api.serializers import TransactionSerializer
from api.exceptions import AuthorisationNotFoundException, AccountNotFoundException
from datetime import datetime


class PaymentService:
    def pay(self, transaction_data):
        transaction_serializer = TransactionSerializer(data=transaction_data)
        if not transaction_serializer.is_valid(): raise Exception('invalid transaction data')
        transaction = Transaction(**transaction_serializer.validated_data)

        if transaction.type == 'authorisation':
            return self._authorize(transaction)
        elif transaction.type == 'presentment':
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
            type='authorisation',
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
