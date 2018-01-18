from django.db import models
from .exceptions import InsuficientFundsException
from decimal import Decimal

class Account(models.Model):
    card_id = models.CharField(max_length=30, default='')
    money = models.DecimalField(max_digits=10, decimal_places=2)
    reserved_money = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    base_currency = models.CharField(max_length=3, default='USD')

    @classmethod
    def create(card_id='', money=0, reserved_money=0, base_currency='USD'):
        account = Account()
        account.card_id = card_id
        account.money = money
        account.reserved_money = reserved_money
        account.base_currency = base_currency
        return account

    def execute_presentment(self, amount):
        can_execute = amount <= self.reserved_money
        if not can_execute: raise InsuficientFundsException
        self.reserved_money -= amount
        self.money -= amount

    def reserve_money(self, amount):
        can_reserve = self.get_available_money() >= Decimal(amount)
        if not can_reserve: raise InsuficientFundsException
        self.reserved_money = (self.reserved_money or 0) + Decimal(amount)

    def get_available_money(self):
        return (self.money or 0) - (self.reserved_money or 0)

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

class Transfer(models.Model):
    destination = models.CharField(30, max_length=30)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency =  models.CharField(30, max_length=3)
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create(cls, destination='', amount=0, currency='USD'):
        transfer = Transfer()
        transfer.destination = destination
        transfer.amount = amount
        transfer.currency = currency
        return transfer