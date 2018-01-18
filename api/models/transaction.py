from django.db import models
from decimal import Decimal

class Transaction(models.Model): 
    TRANSACTION_TYPES = (('A', 'Authorisation'), ('P', 'Presentment'))
    card_id = models.CharField(max_length=30)
    type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)
    transaction_id = models.CharField(max_length=30)
    merchant_mcc = models.CharField(max_length=10)
    billing_amount = models.DecimalField(max_digits=10, decimal_places=2)
    billing_currency = models.CharField(max_length=3)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_currency = models.CharField(max_length=3)
    settlement_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0'))
    settlement_currency = models.CharField(max_length=3, default=None)
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_revenue(self):
        if self.type == 'A': return 0
        return self.billing_amount - self.settlement_amount

    @staticmethod
    def from_json(data):
        transaction = Transaction()
        transaction.transaction_id = data['transaction_id']
        transaction.type = 'A' if data['type'] == 'authorisation' else 'P'
        transaction.merchant_mcc = data['merchant_mcc']
        transaction.card_id = data['card_id']
        transaction.billing_amount = Decimal(data['billing_amount'])
        transaction.billing_currency = data['billing_currency']
        transaction.transaction_amount = Decimal(data['transaction_amount'])
        transaction.transaction_currency = data['transaction_currency']
        transaction.settlement_amount = Decimal(data['settlement_amount']) if transaction.type == 'P' else 0
        transaction.settlement_currency = data['settlement_currency'] if transaction.type == 'P' else 'USD'
        return transaction