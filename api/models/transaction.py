from django.db import models
from decimal import Decimal

class Transaction(models.Model): 
    card_id = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    transaction_id = models.CharField(max_length=30)
    merchant_mcc = models.CharField(max_length=10)
    billing_amount = models.DecimalField(max_digits=10, decimal_places=2)
    billing_currency = models.CharField(max_length=3)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_currency = models.CharField(max_length=3)
    settlement_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0'), null=True)
    settlement_currency = models.CharField(max_length=3, default=None, null=True)
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_revenue(self):
        if self.type == 'A': return 0
        return self.billing_amount - self.settlement_amount