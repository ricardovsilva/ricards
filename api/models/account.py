from django.db import models
from api.exceptions import InsuficientFundsException
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

    def add_money(self, amount, currency):
        '''I choose to create a method to add_money because here it can consume some service
           to provide currency exchange'''
        self.money += amount

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