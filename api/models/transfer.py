from django.db import models

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