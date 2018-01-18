from django.core.management.base import BaseCommand, CommandError
from api.models import Account
from decimal import Decimal

class Command(BaseCommand):
    help = 'Load money to specific account based using card id as primary key'

    def add_arguments(self, parser):
        parser.add_argument('card_id')
        parser.add_argument('amount', type=Decimal)
        parser.add_argument('currency')

    def handle(self, *args, **options):
        import pdb
        pdb.set_trace()
        account = Account.objects.get(card_id=options['card_id'])
        account.add_money(options['amount'], options['currency'])
        account.save()

        self.stdout.write(self.style.SUCCESS('Successfully added ' + options['currency'] + ' to account of card ' + options['card_id']))