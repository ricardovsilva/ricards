from django.db import models
from .exceptions import InsuficientFundsException

class Account(models.Model):
    card_id = models.CharField(max_length=30, default='')
    money = models.DecimalField(max_digits=10, decimal_places=2)
    reserved_money = models.DecimalField(max_digits=10, decimal_places=2)
    base_currency = models.CharField(max_length=3)

    def reserve_money(self, amount):
        pass

    def get_available_money(self):
        pass

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
    settlement_amount = models.DecimalField(max_digits=10, decimal_places=2)
    settlement_currency = models.CharField(max_length=3)
    processed = models.BooleanField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


    @staticmethod
    def from_json(data):
        transaction = Transaction()
        transaction.transaction_id = data['transaction_id']
        transaction.type = 'A' if data['type'] == 'authorisation' else 'P'
        transaction.merchant_mcc = data['merchant_mcc']
        transaction.card_id = data['card_id']
        transaction.billing_amount = data['billing_amount']
        transaction.billing_currency = data['billing_currency']
        transaction.transaction_amount = data['transaction_amount']
        transaction.transaction_currency = data['transaction_currency']
        transaction.settlement_amount = data['settlement_amount'] if transaction.type == 'P' else None
        transaction.settlement_currency = data['settlement_currency'] if transaction.type == 'P' else None
        return transaction